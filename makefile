KWSDemo: MultiClassTsetlinMachine.c UserSetup.h MultiClassTsetlinMachine.h TsetlinMachine.c TsetlinMachine.h search.c
	gcc -Wall -O3 -ffast-math -o hyp_search search.c MultiClassTsetlinMachine.c TsetlinMachine.c 

clean:
	rm *.o hyp_search
