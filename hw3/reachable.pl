walk(A,B) :-  
    walk(A,B,[]). 
walk(A,B,V) :-  
    myedge(A,X) , 
    not(member(X,V)) ,
    (B =:= X ; walk(X,B,[A|V])).

add_rule(Predicate, X, Y) :-
    Fact =.. [Predicate, X, Y],
    assertz(Fact).

build_graph() :-
    read_line_to_string(user_input, S),
    split_string(S, " ", "", L),
    nth0(0, L, X), atom_string(X, A),
    nth0(1, L, Y), atom_string(Y, B),
    add_rule(myedge, A, B),
    add_rule(myedge, B, A).

init_rules() :-
    read_line_to_string(user_input, S),
    split_string(S, " ", "", L),
    nth0(1, L, X), 
    atom_number(X, EDGES),
    foreach(between(1,EDGES,_), build_graph()).

eval_conns() :-
    read_string(user_input, "\n", "", _, S),
    split_string(S, " ", "", L),
    nth0(0, L, X), atom_string(X, A),
    nth0(1, L, Y), atom_string(Y, B),
    (   walk(A,B) 
    ->  format("Yes~n")
    ;   format("No~n")),
    at_end_of_stream(user_input) ; true.

process_query() :-
    read_line_to_string(user_input, S),
    atom_number(S, QUERY),
    foreach(between(1,QUERY,_), eval_conns()).

main() :-
    prompt(_,''),
    init_rules(),
    process_query(),
    halt.

:- initialization(main).
