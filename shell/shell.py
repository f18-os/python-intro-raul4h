import os,sys, time, re

def p4(inp):
    pid = os.getpid()               # get and remember pid

    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

    rc = os.fork()

    print(os.environ['PATH'])
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                     (os.getpid(), pid)).encode())

        os.close(1)                 # redirect child's stdout
        sys.stdout = open("shell-output.txt", "w")
        fd = sys.stdout.fileno() # os.open("shell.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, inp)
            try:
                os.execve(program, inp, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        os.write(2, ("Child:    Error: Could not exec %s\n" % inp).encode())
        sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                     childPidCode).encode())

inp = input("$")
ex = 0

while ex != 1:
    inp = input("$")
    if(inp == "exit"):
        ex = 1
    else:
        p4(inp)
print("Goodbye!")
