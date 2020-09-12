is_prime(N) :-
    N > 2,
    N mod 2 =\= 0,
    MAX is ceiling(sqrt(N)),
    is_prime(N, MAX, 3).
is_prime(N, MAX, X) :-
    X > MAX -> true ;
    N mod X =\= 0,
    is_prime(N, MAX, X+2).

next_prime(P,P1) :- 
    P1 is P + 2, 
    is_prime(P1).
next_prime(P,P1) :- 
    next_prime(P+2,P1).

goldbach(4,[2,2]).
goldbach(N,L) :- 
    N > 4, 
    N mod 2 =:= 0, 
    goldbach(N,L,3).

goldbach(N,[P,Q],P) :- 
    Q is N - P, 
    P < Q,
    is_prime(Q).
goldbach(N,L,P) :- 
    P < N, 
    next_prime(P,P1), 
    goldbach(N,L,P1).

main :-
    prompt(_,''),
    format("Input : "), 
    read_line_to_string(user_input, S),
    atom_number(S,N),
    goldbach(N,L),
    format("Outut : ~w ~w~n", L),
    halt.

:- initialization(main).
