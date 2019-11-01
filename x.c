#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pthread.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/audit.h>
#include <stddef.h>

void* start(void* args){
    
    struct sock_filter filter[] = {
	   /* [0] Load architecture from 'seccomp_data' buffer into
			  accumulator */

	   BPF_STMT(BPF_LD | BPF_W | BPF_ABS,
				(offsetof(struct seccomp_data, instruction_pointer))),

	   /* [1] Jump forward 1 instructions if architecture does not
			  match 't_arch' */
	   BPF_JUMP(BPF_JMP | BPF_JGT | BPF_K, 0x4000, 0, 0),

	   /* [6] Destination of system call number mismatch: allow other
			  system calls */

	   /* [7] Destination of architecture mismatch: kill task */
       BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
	   
   };

   struct sock_fprog prog = {
	   .len = (unsigned short) (sizeof(filter) / sizeof(filter[0])),
	   .filter = filter,
   };
   
   if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
		perror("prctl(NO_NEW_PRIVS)");
		return 1;
	}

   
   if (prctl(PR_SET_SECCOMP, 2, &prog)) {
	   perror("seccomp");
	   return 1;
   }

    while(1){};
}

pthread_t t;

char *map = "/proc/self/maps";
char *test_str = "open";
int main(){
    //start(NULL);
    int fd = open(map, 0);

    char buf[4096];

    int len = read(fd, buf, 4096);
    write(1, buf, len);
    printf("%llx\n", *(long long*)(read+14));


    pthread_create(&t, NULL, start, NULL);
    while(1){};
}
