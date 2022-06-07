/*

Copyright (c) 2019 Ole-Christoffer Granmo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This code implements the Tsetlin Machine from paper arXiv:1804.01508
https://arxiv.org/abs/1804.01508

*/
//
//#define THRESHOLD 2
//#define FEATURES 377
//#define CLAUSES 50
//#define NUMBER_OF_STATES 100
//#define BOOST_TRUE_POSITIVE_FEEDBACK 1
//
//#define PREDICT 1
//#define UPDATE 0
#include "UserSetup.h"
#include <stdio.h>
#include <stdlib.h>

struct TsetlinMachine { 
	short ta_state[CLAUSES][FEATURES][2];

	char clause_output[CLAUSES];

	char feedback_to_clauses[CLAUSES];
};

struct TsetlinMachine *CreateTsetlinMachine();

void tm_initialize(struct TsetlinMachine *tm);

void tm_save_ta(struct TsetlinMachine *tm,   FILE *pFile);

void tm_load_ta(struct TsetlinMachine *tm,  int saved_states[], int class_idx);

void tm_update(struct TsetlinMachine *tm, int Xi[], int target, float s);

int tm_score(struct TsetlinMachine *tm, int Xi[]);

int tm_get_state(struct TsetlinMachine *tm, int clause, int feature, int automaton_type);
void tm_load_state(struct TsetlinMachine *tm, int clause, int feature, int automaton_type, short state);

