(*
 * expr.ml
 * cse130
 * based on code by Chris Stone
 *)

(* REMEMBER TO DOCUMENT ALL FUNCTIOONS THAT YOU WRITE OR COMPLETE *)

type expr = 
    VarX
  | VarY
  | Sine     of expr
  | Cosine   of expr
  | Average  of expr * expr
  | Times    of expr * expr
  | Thresh   of expr * expr * expr * expr
  | ExpNegAbs of expr
  | LogPlus  of expr * expr * expr

(* exprToString: expr -> string
   Takes an expression and converts it to a string for printing.
*)
let rec exprToString e =
  match e with
   VarX -> "x"
    | VarY -> "y"
    | Sine x -> String.concat "" ["sin(pi*";exprToString x;")"]
    | Cosine x -> String.concat "" ["cos(pi*";exprToString x;")"]
    | Average (x,y) -> String.concat "" ["((";exprToString x;"+";exprToString y;")/2)"]
    | Times (x,y) -> String.concat "" [exprToString x;"*";exprToString y]
    | Thresh (e1,e2,e3,e4) -> String.concat "" ["(";exprToString e1;"<";exprToString e2;"?";exprToString e3;":";exprToString e4;")"]
    | ExpNegAbs (e) -> String.concat "" ["10^-abs(";exprToString e;")"]
    | LogPlus (e1,e2,e3) -> String.concat "" ["(ln (1.5+(";exprToString e1;"))+(ln(1.5+(";exprToString e2;")))+(ln(1.5+(";exprToString e3;"))))/3"]

(* build functions:
     Use these helper functions to generate elements of the expr
     datatype rather than using the constructors directly.  This
     provides a little more modularity in the design of your program *)

let buildX()                       = VarX
let buildY()                       = VarY
let buildSine(e)                   = Sine(e)
let buildCosine(e)                 = Cosine(e)
let buildAverage(e1,e2)            = Average(e1,e2)
let buildTimes(e1,e2)              = Times(e1,e2)
let buildThresh(a,b,a_less,b_less) = Thresh(a,b,a_less,b_less)
let buildExpNegAbs(e)		   = ExpNegAbs(e)
let buildLogPlus(e1,e2,e3)         = LogPlus(e1,e2,e3)


let pi = 4.0 *. atan 1.0

(* eval: expr * float * float -> float
   Takes a triple (e,x,y) and evaluates the expression e at the point
   x, y.
*)
let rec eval (e,x,y) = 
  match e with
    VarX -> x
    | VarY -> y
    | Sine e1 -> sin (pi *. eval (e1,x,y))
    | Cosine e1 -> cos (pi *. eval (e1,x,y))
    | Average (e1,e2) -> ((eval (e1,x,y)) +. (eval (e2,x,y)))/. 2.0
    | Times (e1,e2) -> (eval (e1,x,y)) *. (eval (e2,x,y))
    | Thresh (e1,e2,e3,e4) -> if (eval (e1,x,y))<(eval (e2,x,y)) then eval (e3,x,y) else eval (e4,x,y)
    | ExpNegAbs (e) -> (10.0**(-.abs_float (eval (e,x,y))))
    | LogPlus (e1,e2,e3) -> (log (1.5 +. (eval (e1, x, y)))+. log (1.5 +. (eval (e2, x, y)))+.log (1.5 +. (eval (e3, x, y))))/.3.0

(* (eval_fn e (x,y)) evaluates the expression e at the point (x,y) and then
 * verifies that the result is between -1 and 1.  If it is, the result is returned.  
 * Otherwise, an exception is raised.
 *)
let eval_fn e (x,y) = 
  let rv = eval (e,x,y) in
  assert (-1.0 <= rv && rv <= 1.0);
  rv

let sampleExpr =
      buildCosine(buildSine(buildTimes(buildCosine(buildAverage(buildCosine(
      buildX()),buildTimes(buildCosine (buildCosine (buildAverage
      (buildTimes (buildY(),buildY()),buildCosine (buildX())))),
      buildCosine (buildTimes (buildSine (buildCosine
      (buildY())),buildAverage (buildSine (buildX()), buildTimes
      (buildX(),buildX()))))))),buildY())))

let sampleExpr2 =
  buildThresh(buildX(),buildY(),buildSine(buildX()),buildCosine(buildY()))


(************** Add Testing Code Here ***************)
