(* CSE 130: Programming Assignment 1
 * misc.ml
 * Ryan Fisher
 * PID: U05031030
 *)

(* sumList : int list -> int 
 * (sumList l) is the summation of the elements of an int list
 * e.g. (sumList [5;2;9;3]) is 19
 *      (sumList [3;17;2;8;1;3]) is 34
 *) 

let rec sumList l =
    match l with
    | []  -> 0
    | h::t -> h+sumList t
;;

(* digitsOfInt : int -> int list 
 * (digitsOfInt n) is the a list of the digits in n
 * 0 and negative values of n return []
 * e.g. (digitsOfInt 34587) is [3;4;5;8;7]
 *      (digitsOfInt (-238) is []
 *)

let rec digitsOfInt n = 
    if n<=0 then
        []
    else
        digitsOfInt (n/10)@[n mod 10]
;;


(* digits : int -> int list
 * (digits n) is the list of digits of n in the order in which they appear
 * in n
 * e.g. (digits 31243) is [3,1,2,4,3]
 *      (digits (-23422) is [2,3,4,2,2]
 *)
 
let digits n = digitsOfInt (abs n);;


(* From http://mathworld.wolfram.com/AdditivePersistence.html
 * Consider the process of taking a number, adding its digits, 
 * then adding the digits of the number derived from it, etc., 
 * until the remaining number has only one digit. 
 * The number of additions required to obtain a single digit from a number n 
 * is called the additive persistence of n, and the digit obtained is called 
 * the digital root of n.
 * For example, the sequence obtained from the starting number 9876 is (9876, 30, 3), so 
 * 9876 has an additive persistence of 2 and a digital root of 3.
 *)


(* ***** PROVIDE COMMENT BLOCKS FOR THE FOLLOWING FUNCTIONS ***** *)

(* sumDigits : int -> int
 * (sumDigits n) is the summation of the digits of n
 * e.g. (sumDigits 31243) is 13
 *      (sumDigits (-23422)) is 13
 *)
let sumDigits n = sumList (digits n);;

(* additivePeristence : int -> int
 * (additivePersistence n) is the number of additions it takes to reach
 * the digital root. That is, taking a number, adding its digits, and 
 * repeating this process until reaching a single digit.
 * e.g. (additivePersistence 9876) is 2
 *      (additivePersistence 18) is 1
 *)
let rec additivePersistence n = 
     if n<10 then
          0
     else
          1+(additivePersistence (sumDigits n))
;;

(* digitalRoot : int -> int
 * (digitalRoot n) is the single digit achieved from the process
 * of taking a number, adding its digits, then adding the digits of
 * the number derived from it, etc.
 *)
let rec digitalRoot n = 
     if n<10 then
          n
     else
          digitalRoot (sumDigits n)
;;

(* listReverse : 'a list -> 'a list
 * (listReverse l) is the reverse of list l
 * e.g. (listReverse [5;2;8;1]) is [1;8;2;5]
 *      (listReverse ["ab";"a";"rt"]) is ["rt";"a";"ab"]
 *)
let listReverse l = 
  match l with
    | h::t -> listReverse t@[h]
    | _ -> []
;;

(* explode : string -> char list 
 * (explode s) is the list of characters in the string s in the order in 
 *   which they appear
 * e.g.  (explode "Hello") is ['H';'e';'l';'l';'o']
 *)
let explode s = 
  let rec _exp i = 
    if i >= String.length s then [] else (s.[i])::(_exp (i+1)) in
  _exp 0
;;

(* palindrome : string -> bool
 * (palindrome w) is true if w is a palindrome and false otherwise
 * e.g. (palindrome "Ryan Fisher") is false
 *      (palindrome "racecar") is true
 *)
let palindrome w = (explode w=listReverse (explode w));;

(************** Add Testing Code Here ***************)
