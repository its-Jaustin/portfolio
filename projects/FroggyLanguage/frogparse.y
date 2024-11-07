%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct Variable{
	char* var_name;
	float value;
};

struct Variable table[100];
int table_index = 0;

/*function declarations*/
void yyerror(const char* s);
void output(float num);
float get(char* var_name);
void set(char* var_name, float value);
float to_decimal(int num);
int isInt(float num);
extern int yylex();


%}
%union{
	float number;
	char* string;
	int b_num;
}

%token ADD SUBTRACT MULTIPLY DIVIDE CONVERT ASSIGN OPEN_PREN CLOSE_PREN
%token VARIABLE_NAME OUTPUT_COMMAND END_OF_STATEMENT PERIOD
%token ZERO ONE
%token FLOAT_TYPE INT_TYPE
%type<string> VARIABLE_NAME
%type<number> expression term factor num Float
%type<b_num> binaryNum
%left ADD SUBTRACT
%left MULTIPLY DIVIDE
%left CONVERT
%left OPEN_PREN CLOSE_PREN


%%
program:	statement_list
		;
statement_list: statement
		| statement statement_list
		;
statement: 	expression END_OF_STATEMENT
		| assignment END_OF_STATEMENT 
		| output END_OF_STATEMENT
		;
output:		OUTPUT_COMMAND expression	{output($2);}
		;
assignment: 	VARIABLE_NAME ASSIGN expression	{printf("Assignment: %s ~ %.3f\n", $1, $3);set($1,$3);}
		;
expression: 	term ADD expression		{$$ = $1 + $3;} 
		| term SUBTRACT expression 	{$$ = $1 - $3;}
		| term
		|expression CONVERT INT_TYPE	{printf("Converting %f to int\n", $1);$$ = (float)((int)$1);}
		|expression CONVERT FLOAT_TYPE {$$ = $1;}
		;
term:		factor MULTIPLY term 		{$$ = $1 * $3;}
		| factor DIVIDE DIVIDE term 	{if(isInt($1) && isInt($4)){$$= (float)(((int)$1) / ((int)$4));}else{$$=$1/$4;} }
		| factor DIVIDE term		{$$ = $1 / $3;}
		| factor
		;
factor:		num 		{$$ = $1;} 
		| OPEN_PREN  expression CLOSE_PREN {$$ = $2;} 
		| VARIABLE_NAME {$$ = get($1);}
		;
num:		binaryNum 	{$$ = (float)$1;} 
		| Float
		;
Float:		binaryNum PERIOD binaryNum 	{ $$ = (float)$1 + to_decimal($3);}
		;	
binaryNum:	binaryNum ZERO 	{$$ = $1 * 2 + 0;} //Append 0 (shift left 1)
		|binaryNum ONE 	{$$ = $1 * 2 + 1;} //Append 1 (shift left 1 add 1)
		|ZERO 		{$$ = 0;}
		|ONE 		{$$ = 1;}
		;

%%
int isInt(float num){
	if (num == (int)num){return 1;}
	return 0;
}
void output(float num){
	if (num == (int)num){
		printf("Output -->%d\n", (int)num);
	}else{
		printf("Output -->%f\n", num);
	}
}
float get(char* var_name){
	/*for now this will just be O(n) search*/
	for (int i=0; i<table_index; ++i){
		if (strcmp(table[i].var_name, var_name) == 0) { 
			return table[i].value;
		}
        }
    	printf("Error: Variable %s not found\n", var_name);
    	exit(1);
}
void set(char* var_name, float value){
	if (table_index >= 100){
		printf("Error: Exceeded variable limit");
		exit(1);
	}
	//printf("Var name: %s  Value: %.2f\n", var_name, value);
	table[table_index].var_name = strdup(var_name);
	table[table_index].value = value;
	table_index++;
}
float to_decimal(int num){
	float my_num = (float)num;
	while (my_num >= 1.0){
		my_num /= 10;
	}
	//printf("My decimal %f", my_num);
	return my_num;
}
void yyerror(const char* s){

     fprintf(stderr, "Syntax error: %s\n", s);
}
int main(int argc, char** argv){
	yyparse();
}


