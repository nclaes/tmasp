
#include "UserSetup.h"
#include "MultiClassTsetlinMachine.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#define MAX_FILE_NAME 100
#include <string.h>
long long int Numof_TA  = FEATURES*2*CLASSES*CLAUSES;

int X_Train[NUMBER_OF_EXAMPLES][FEATURES];
int Y_Train[NUMBER_OF_EXAMPLES];

int X_Vali[NUMBER_OF_VALI_EXAMPLES][FEATURES];
int Y_Vali[NUMBER_OF_VALI_EXAMPLES];

void read_file(void)
{
    FILE * fp;
	char * line = NULL;
	size_t len = 0;
	const char *s = " ";
	char *token = NULL;

    fp = fopen("Boolean_datasets/mnist_train.txt", "r");
	if (fp == NULL) {
		printf("Error opening\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < NUMBER_OF_EXAMPLES; i++) {
		getline(&line, &len, fp);

		token = strtok(line, s);
		for (int j = 0; j < FEATURES; j++) {
			X_Train[i][j] = atoi(token);
			token=strtok(NULL,s);
		}
		Y_Train[i] = atoi(token);
	}

	fp = fopen("Boolean_datasets/mnist_test.txt", "r");
	if (fp == NULL) {
		printf("Error opening\n");
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < NUMBER_OF_VALI_EXAMPLES; i++) {
		getline(&line, &len, fp);

		token = strtok(line, s);
		for (int j = 0; j < FEATURES; j++) {
			X_Vali[i][j] = atoi(token);
			token=strtok(NULL,s);
		}
		Y_Vali[i] = atoi(token);
	}
}

int count_includes(struct MultiClassTsetlinMachine *mc_tm)
{
	int count = 0;
	for(int i = 0; i < CLASSES; i++)
	{
		for(int j = 0; j < CLAUSES; j++)
		{
			for (int k = 0; k < FEATURES; k++) 
			{
				if(( (mc_tm->tsetlin_machines[i])->ta_state[j][k][0] ) > NUMBER_OF_STATES)
					{
						count++;
					}
				if(( (mc_tm->tsetlin_machines[i])->ta_state[j][k][1] ) > NUMBER_OF_STATES)
					{
						count++;
					}
			}
		}
	}
	return count;
}

int main(void)
{
	srand(time(NULL));
	read_file();
	struct MultiClassTsetlinMachine *mc_tsetlin_machine = CreateMultiClassTsetlinMachine();
    // mc_tm_initialize(mc_tsetlin_machine);
	// float average = 0.0;
	float current = 0.0;
	int num_includes = 0;
	for (int i = 0; i < EPOCHS; i++) {
        mc_tm_fit(mc_tsetlin_machine, X_Train, Y_Train, NUMBER_OF_EXAMPLES, 1, S);
	}
    current = mc_tm_evaluate(mc_tsetlin_machine, X_Vali, Y_Vali, NUMBER_OF_VALI_EXAMPLES); 
    char file_name[100];
    sprintf(file_name, "MNIST_TA_FILE_C%d_S%d_T%d_E%d.txt", (int)CLAUSES, (int)S, (int)THRESHOLD, (int)EPOCHS);
    FILE * fp;
    fp = fopen(file_name, "w");

    mc_tm_save_ta(mc_tsetlin_machine, fp);   
    num_includes = count_includes(mc_tsetlin_machine);
    printf("Accuracy %f\n", current*100);
    printf("Includes %d\n", num_includes);
    return 0;
}
