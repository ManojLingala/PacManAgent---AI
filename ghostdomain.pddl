(define (domain ghost)

    (:requirements
        :strips
    )

    (:predicates
    (at ?x ?y) ;co-ordinates of ghost's position
    (eaten ?p) ;whether or not a pacman has been eaten
    (inc ?x1 ?x2) ;x-coordinate changes
    (dec ?y1 ?y2) ;y-coordinate changes
    (wall ?x ?y) ;wall co-ordinates
    (pacmanat ?p ?x ?y) ;pacman's co-ordinates
    )

    ;can only move in a certain direction if there are no walls, and if the x or y co-ordinate for the next
    ;position matches the direction moved

    (:action move-right
        :parameters (?x1 ?x2 ?y)
        :precondition (and (at ?x1 ?y) (not (wall ?x2 ?y)) (inc ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-left
        :parameters (?x1 ?x2 ?y)
        :precondition (and (at ?x1 ?y) (not (wall ?x2 ?y)) (dec ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-up
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (inc ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )
    
    (:action move-down
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (dec ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )

    (:action eat
        :parameters (?x ?y ?p)
        :precondition (and (pacmanat ?p ?x ?y) (at ?x ?y))
        :effect (and (eaten ?p) (not (pacmanat ?p ?x ?y)))
    )
    )