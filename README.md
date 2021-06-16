# checker
GUI checker
This is a gui interface for draughts, which is relatively simple to do.

The game interface is divided into two parts, the left is the chessboard, and the right is the operation interface.The chessboard is an 8x8 interface, in which the red chess pieces are operated by the user, ''and the white pieces are operated by the AI. The green dot indicates that the current user can move. The blue dots indicate. Actions that can be performed by selecting a piece.

The input box on the first line of the operation interface indicates the piece you want to operate (for example, input (5,0) at the beginning of the game),and then you can click the check button to check whether the piece can be moved, and the board will be blue Click (if the chess piece can be moved), the operation interface will also prompt (output the position that can be moved). The input in the second line represents the coordinates of the move of the chess piece input in the first line. Then the user can click the move button to move.The bottom slider and buttons can adjust the difficulty (the game will not be restarted).

Black moves first and play proceeds alternately. From their initial positions, checkers may only move forward. There are two types of moves that can be made, capturing moves and non-capturing moves. Non-capturing moves are simply a diagonal move forward from one square to an adjacent square. (Note that the white squares are never used.) Capturing moves occur when a player "jumps" an opposing piece. This is also done on the diagonal and can only happen when the square behind (on the same diagonal) is also open. This means that you may not jump an opposing piece around a corner.Capturing Move On a capturing move, a piece may make multiple jumps. If after a jump a player is in a position to make another jump then he may do so. This means that a player may make several jumps in succession, capturing several pieces on a single turn.Forced Captures: When a player is in a position to make a capturing move, he must make a capturing move. When he has more than one capturing move to choose from he may take whichever move suits him')


        
