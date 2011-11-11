(* CSE 130: Programming Assignment 2
 * misc.ml
 *)

(* ***** DOCUMENT ALL FUNCTIONS YOU WRITE OR COMPLETE ***** *)
(* assoc: int * string * (string * int) list -> int
   Takes a triple (d,k,l) where l is a list of key-value pairs
   and finds the first key that equals k. If found, the corresponding
   value is returned. Otherwise, the default value d is returned.
*)
let rec assoc (d,k,l) = 
  match l with
     [] -> d
    | (n,num)::t -> if n = k then num else assoc (d,k,t)

(* removeDuplicates: int list -> int list
   Takes a list l and returns the list of elements of l
   with duplicates
 *)
let removeDuplicates l = 
  let rec helper (seen,rest) = 
      match rest with 
        [] -> seen
      | h::t -> 
        let seen' = if List.mem h seen then seen else h::seen in
        let rest' = t in 
	  helper (seen',rest') 
  in
      List.rev (helper ([],l))


(* Small hint: see how ffor is implemented below *)
(* wwhile: (int -> int * bool) * int -> int
   Takes as input a pair (f,b) and calls the function f on input
   b to get a pair (b', c'). wwhile should continue calling f on b'
   to update the pair as long as c' is true. Once f returns a c'
   that is false, wwhile should return b'.
*)
let rec wwhile (f,b) =
  let tu = f b in
    match tu with
     (fi,se) -> if se then wwhile (f,fi) else fi

(* fixpoint: (int -> int) * int -> int
   Repeatedly updates b with f(b) until b=f(b) and then returns b.
*)
let fixpoint (f,b) = wwhile ((failwith "to be written"),b)


(* ffor: int * int * (int -> unit) -> unit
   Applies the function f to all the integers between low and high
   inclusive; the results get thrown away.
 *)

let rec ffor (low,high,f) = 
  if low>high 
  then () 
  else let _ = f low in ffor (low+1,high,f)
      
(************** Add Testing Code Here ***************)
