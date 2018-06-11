(define (problem pacman0)

  (:domain ghost)

  (:objects x1 x2 x3 x4 x5 y1 y2 y3 y4 y5 p1 p2) ;x and y co-ordinates, pacman names
  
  ;lays out the 5x5 grid and defines which movements will end in which positions.

  (:init

    (inc x1 x2) (inc x2 x3) (inc x3 x4) (inc x4 x5)

    (inc y1 y2) (inc y2 y3) (inc y3 y4) (inc y4 y5)

    (dec x5 x4) (dec x4 x3) (dec x3 x2) (dec x2 x1) 

    (dec y5 y4) (dec y4 y3) (dec y3 y2) (dec y2 y1)

    (at x1 y1)
    
    (wall x3 y3) (wall x4 y3) (wall x5 y3) (pacmanat p1 x3 y5) (pacmanat p2 x5 y1))

  (:goal

    (and (eaten p1) (eaten p2))

  )
  )