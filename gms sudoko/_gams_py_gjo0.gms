
set
    i/1*9/;
alias(i,j,k);

Parameter
    n(i,j);

$GDXIN %gdxincname%
$LOAD n
$GDXIN

integer variable
    result,
    v(i,j);
variable
    z;

binary variable
*x[i,j,k] = 1 -> x(i,j) = k
    x(i,j,k);

integer variable
    v(i,j);

equation
    obj,
    const1,
    const2,
    const3
    const4,
    const5;

obj..
    z =e= 0;

*satr va sotoon
const1(j,k)..
    sum(i,x(i,j,k)) =e= 1;
const2(i,k)..
    sum(j,x(i,j,k)) =e= 1;
const3(i,j)..
    sum(k,x(i,j,k)) =e= 1;

const4(i,j,k)$(n(i,j)=k.val)..
    x(i,j,k) =e= 1;

*block
const5(i,j,k)$( (i.val = 1 or i.val = 4 or i.val = 7) and (j.val = 1 or j.val = 4 or j.val = 7) )..
    x(i,j,k)+x(i,j+1,k)+x(i,j+2,k)+x(i+1,j,k)+x(i+1,j+1,k)+x(i+1,j+2,k)+x(i+2,j,k)+x(i+2,j+1,k)+x(i+2,j+2,k) =e= 1;


model sudoku/obj, const1, const2, const3, const4, const5/;
solve sudoku using MIP minimizing z;
