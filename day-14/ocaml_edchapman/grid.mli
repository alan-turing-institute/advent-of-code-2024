(** Zero-indexed grid, with locations [(x,y)] where x increases rightwards and y increases downwards, i.e. the top-left is [(0,0)]. *)

type 'a t
(** The grid. *)

type loc = int * int
(** [(x,y)] where x increases rightwards, and y increases downwards. [(0,0)] is top-left. *)

type size = int * int
(** [(width,height)]. *)

type dir =
  | Up
  | Right
  | Down
  | Left

val of_lss : 'a list list -> 'a t
(** [of_lss lss] is a grid. [lss] must be in the following configuration:

  [ [[ (0,0); (1,0); (2,0) ];
     [ (0,1); (1,1); (2,1) ];
     [ (0,2); (1,2); (2,2) ]] ]
*)

val size : 'a t -> size
(** [size grid] is [(width,height)]. *)

val off_grid : size -> loc -> bool
val on_grid : size -> loc -> bool

val wrap : size -> loc -> loc
(** [wrap (w,h) (x,y)] is a location that is guaranteed to be on the grid of width [w] and height [h]. Negative co-ordinates and co-ordinates larger than the grid are 'wrapped' back onto the grid. *)

val ( +@ ) : loc -> loc -> loc
(** Elementwise add grid locations. *)

val ( -@ ) : loc -> loc -> loc
(** Elementwise subtract grid locations. *)

val delta : loc -> loc -> loc
(** [delta (ax,ay) (bx,by)] is [(bx-ax),(by-ay)]. *)

val eq : loc -> loc -> bool
(** [eq (ax,ay) (bx,by)] is [true] iff [ax=bx] and [ay=by] (i.e. element-wise structural equality). *)

val all_locations : 'a -> 'a t -> loc list
(** [all_locations x grid] is all locations where the value in the grid [=x] (i.e. structural equality). *)

val fold : ('acc -> 'a -> 'acc) -> 'acc -> 'a t -> 'acc
(** Fold from the top, left-folding each row. *)

val mapi : (loc -> 'a -> 'b) -> 'a t -> 'b t
val foldi : ('acc -> loc -> 'a -> 'acc) -> 'acc -> 'a t -> 'acc
val print_loc : loc -> unit
val at : 'a t -> loc -> 'a

val move : loc -> dir -> loc
(** [move (x,y) Down] is [(x,y+1)] (because [(x,y):loc] has y increasing downwards, i.e. [(0,0)] is top-left. *)

val move_delta : delta:int * int -> loc -> loc
(** [move_delta ~delta:(dx,dy) (x,y)] is [(x+dx, y+dy)], where all values may be positive or negative. *)
