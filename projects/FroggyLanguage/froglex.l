%{
#include <stdlib.h>
#include "frogparse.tab.h"
extern int yylex();
%}
%%
#.*?  { ; }
[ \t\n\r]+     { ; }
froggy[A-Za-z0-9_]{1,20}froG     { yylval.string = strdup(yytext); return VARIABLE_NAME;}
(Toad)						{ return ZERO; }
(FROG) 						{ return ASSIGN;}
(fwog)						{ return OUTPUT_COMMAND; }
(FRog)						{ return PERIOD; }
(froggY)					{ return END_OF_STATEMENT; }
(froage)	{ return OPEN_PREN; }
(froagy)	{ return CLOSE_PREN; }
(make)		{ return CONVERT; }
(Happy)		{ return INT_TYPE; }
(Sad) 		{ return FLOAT_TYPE;}
(Hop)		{ return DIVIDE;}
(Boing)		{ return MULTIPLY;}
(Croak)		{ return SUBTRACT;}
(Ribbit)	{ return ADD;}
(Kermit|exit|quit)	{ exit(0);}
(Frog)		{ return ONE; }

%%


