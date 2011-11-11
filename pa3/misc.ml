(* CSE 130: Programming Assignment 3
 * misc.sml
 *)

(* For this assignment, you may use the following library functions:

   List.map
   List.fold_left
   List.fold_right
   List.split
   List.combine
   List.length
   List.append

   See http://caml.inria.fr/pub/docs/manual-ocaml/libref/List.html for documentation.
*)

(*****************************************************************)
(******************* 1. Warm Up   ********************************)
(*****************************************************************)
(* sqsum: int list -> int
 * Sums the squares of all values in a int list.
 *)
let sqsum xs = 
  let f b x = x*x + b in
  let base = 0 in
  List.fold_left f base xs

(* pipe: ('a -> 'a) list -> ('a -> 'a)
 * Takes a list of functions [f1;...;fn] and returns a function f such that 
 * for any x, the application f x returns the result fn(...(f2(f1 x))).
 *)
let pipe fs = 
  let f b x = fun y -> (x (b y)) in
  let base = fun x -> x in
  List.fold_left f base fs

(* sepConcat: string -> string list -> string
 * Takes as input a string sep to be used as a separator, and a list
 * of strings [s1;...;sn]. If there are 0 strings in the list, then
 * sepConcat should return "".
 *)
let rec sepConcat sep sl = 
   match sl with 
       [] -> ""
     | (h::t) -> 
	 let f b x = b ^ sep ^ x in
	 let base = h in
	 let l = t in
	   List.fold_left f base l

(* stringOfList: ('a -> string) -> 'a list -> string
 * Returns a string representation of the list l as a concatenation of
 * the following: "[" (f l1) ";" (f l2) ";" ... ";" (f ln) "]".
 *)
let stringOfList f l = "["^sepConcat "; " (List.map f l)^"]"

(*****************************************************************)
(******************* 2. big numbers ******************************)
(*****************************************************************)

(* clone: 'a -> int -> 'a list
 * Takes an input x and an integer n and produces a list of length
 * n, where each element is x.
 *)
let rec clone x n =
	if n <= 0 then [] else x::(clone x (n-1))

(* padZero: int list -> int list -> int list * int list
 * Takes two lists and adds zeros in front to make the lists
 * equal.
 *)
let rec padZero l1 l2 = 
	if (List.length l1) = (List.length l2) 
	then (l1,l2) else
		if (List.length l1) < (List.length l2) 
		then (padZero (0::l1) l2)
		else (padZero l1 (0::l2))

(* removeZero: int list -> int list
 * Takes a list and removes all prefixed zeros.
 *)
let rec removeZero l = 
	match l with
	| h::t -> if h = 0 then (removeZero t) else l
	| _ -> []

(* bigAdd: int list -> int list -> int llist
 * Takes two integer lists, where each integer is in the range [0..9]
 * and returns the list corresponding to the addition of the two big 
 * integers.
 *)
let bigAdd l1 l2 = 
  let add (l1,l2) = 
    let f b x = let c = (fst x + snd x) in
	match b with
	| h::t -> ((h+c)/10)::((h+c) mod 10)::t
	| _ -> (c/10)::[c mod 10]
    in
    let base = [] in
    let args = List.rev (List.combine l1 l2) in
    (*let (_,res) = *)(List.fold_left f base args)(* in
      res*)
  in 
    removeZero (add (padZero l1 l2))

(* mulByDigit: int -> int list -> int list
 * Takes an integer digit and a big integer, and returns the integer
 * list which is the result of multiplying the big integer with the 
 * digit.
 *)
let mulByDigit i l = 
    let f b x = let c = i*x in 
	match b with
	| h::t -> ((h+c)/10)::((h+c) mod 10)::t
	| _ -> (c/10)::[c mod 10]
    in
    let base = [] in
    removeZero (List.fold_left f base (List.rev l))

(* bigMul: int list -> int list -> int list
 * Multiplies two big integers.
 *)
let bigMul l1 l2 =
  let g =
  let f b x = ((mulByDigit x l1)@(clone 0 (List.length b)))::b in
  let base = [] in
  let args = List.rev l2 in
  (*let (_,res) = *)(List.fold_left f base args)(* in
    res*)
  in
	List.fold_left bigAdd [] g

