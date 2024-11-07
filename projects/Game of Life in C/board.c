#include "board.h"
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>


Board* update_board(Board* board)
{
    

    char neighbor(Board*,int,int);
    
    int rows = (*board).nrows;
    int cols = (*board).ncols;
    Board* b = board;//did this to make it easier to copy paste

    char* newGrid;
    newGrid = (char *) malloc(rows * cols * sizeof(char));
    
    for(int r=0; r<rows; r++)
    {
        for(int c=0; c<cols; c++)
        {
            //check neighbors
            int green=0, red=0, numNeighbors;
            //north
            int rCoord=r;
            int cCoord=c;
            if(--rCoord<0)
            {
                rCoord = rows-1;
            }
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;
            
            //northwest
            if(--cCoord<0)
            {
                cCoord = cols-1;
            }
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;
            
            //west
            if(++rCoord==rows) rCoord = 0;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            //southwest
            if(++rCoord==rows) rCoord = 0;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            //south
            if(++cCoord==cols) cCoord = 0;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            //southeast
            if(++cCoord==cols) cCoord = 0;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            //east
            if(--rCoord<0) rCoord=rows-1;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            //north east
            if(--rCoord<0) rCoord=rows-1;
            if(neighbor(b, rCoord, cCoord) == 'g') green++;
            else if(neighbor(b, rCoord, cCoord) == 'r') red++;

            numNeighbors = green + red;
    

            //printf("r: %d c: %d n: %d\n", r, c, numNeighbors);

            //populate new board
            if (numNeighbors <2 || numNeighbors > 3) *(newGrid+(r*cols) + c) = 'x';
            else if (numNeighbors == 3 && *((*b).grid+(r*cols) + c) == 'x')
            {
                if(green>red) *(newGrid+(r*cols) + c) = 'g';
                else *(newGrid+(r*cols) + c) = 'r';
            }
            else
            {
                *(newGrid+(r*cols) + c) = *((*b).grid+(r*cols) + c);
            }


        }
    }
    

    free((*board).grid);
    (*board).grid = newGrid;
    


    return board;

}
char neighbor(Board* b, int x, int y){
    int cols = (*b).ncols;
    return *((*b).grid+(x*cols) + y);

}

