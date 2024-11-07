#include <stdio.h>
#include <stdlib.h>
#include "board.h"

Board* board_init(Board *, FILE *, int*);
void print_board(Board *);
void output_colors(Board *);

int main(void)
{
    //FILE * input =  fopen("input.txt", "r");
    FILE * input = stdin;

    Board board;
    
    int numSteps;

    board_init(&board, input, &numSteps);
    
    //fclose(input);

    //printf("Rows: %d Cols: %d grid addy: %p\n", board.nrows, board.ncols, board.grid);
    //printf("Num Steps: %d\n", numSteps);

    //print_board(&board);
    
    //update board for numSteps
    for(int i=0;i<numSteps;i++)update_board(&board);
    

    //output number of colors
    output_colors(&board);


    free(board.grid);
    return 0;
}
Board* board_init(Board* board, FILE* input, int* steps)
{   
    //scan board size and allocate memory for that board
    int rows, cols;
    fscanf(input, "%d %d", &rows, &cols);

    (*board).nrows = rows;
    (*board).ncols = cols;

    (*board).grid = (char *) malloc(rows * cols * sizeof(char));
    //scan number of steps
    fscanf(input, "%d", steps);

    //scan all inital board values
    for(int i = 0; i<(rows*cols); i++)
    {   
        fscanf(input, " %c", ((*board).grid+i));
    }
    



    return board;
}
void print_board(Board* board)
{
    int rows = (*board).nrows;
    int cols = (*board).ncols;

    for(int r = 0; r<rows; r++)
    {
        for(int c=0; c<cols; c++)
        {
            printf("%c ", *((*board).grid+(r*cols) + c));
        }
        printf("\n");
    }

    return;
}
void output_colors(Board* board)
{
    int rows = (*board).nrows;
    int cols = (*board).ncols;

    int green=0, red=0;

    for(int i=0; i<(rows*cols); i++)
    {
        if(*((*board).grid+i) == 'g') green++;
        else if(*((*board).grid+i) == 'r') red++;
    }
    printf("green: %d, red: %d\n", green, red);
    return;
}











