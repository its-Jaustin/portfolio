#ifndef BOARD_H
#define BOARD_H

typedef struct Board {
    int nrows;
    int ncols;
    char *grid;

} Board;

Board* update_board(Board *);



#endif
