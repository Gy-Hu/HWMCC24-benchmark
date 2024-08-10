
;r0
; 

(let ((?x28 (ite (= ((_ extract 3 2) inst) (_ bv2 2)) r2 r3)))
(let ((?x30 (ite (= ((_ extract 3 2) inst) (_ bv0 2)) r0 (ite (= ((_ extract 3 2) inst) (_ bv1 2)) r1 ?x28))))
(let ((?x21 (ite (= ((_ extract 5 4) inst) (_ bv2 2)) r2 r3)))
(let ((?x23 (ite (= ((_ extract 5 4) inst) (_ bv0 2)) r0 (ite (= ((_ extract 5 4) inst) (_ bv1 2)) r1 ?x21))))
(let ((?x32 (ite (= ((_ extract 1 0) inst) (_ bv0 2)) (bvadd ?x23 ?x30) r0)))
?x32)))))


;r1
; 
 (let ((?x28 (ite (= ((_ extract 3 2) inst) (_ bv2 2)) r2 r3)))
(let ((?x30 (ite (= ((_ extract 3 2) inst) (_ bv0 2)) r0 (ite (= ((_ extract 3 2) inst) (_ bv1 2)) r1 ?x28))))
(let ((?x21 (ite (= ((_ extract 5 4) inst) (_ bv2 2)) r2 r3)))
(let ((?x23 (ite (= ((_ extract 5 4) inst) (_ bv0 2)) r0 (ite (= ((_ extract 5 4) inst) (_ bv1 2)) r1 ?x21))))
(let ((?x32 (ite (= ((_ extract 1 0) inst) (_ bv1 2)) (bvadd ?x23 ?x30) r1)))
?x32)))))


;r2
; 
 (let ((?x28 (ite (= ((_ extract 3 2) inst) (_ bv2 2)) r2 r3)))
(let ((?x30 (ite (= ((_ extract 3 2) inst) (_ bv0 2)) r0 (ite (= ((_ extract 3 2) inst) (_ bv1 2)) r1 ?x28))))
(let ((?x21 (ite (= ((_ extract 5 4) inst) (_ bv2 2)) r2 r3)))
(let ((?x23 (ite (= ((_ extract 5 4) inst) (_ bv0 2)) r0 (ite (= ((_ extract 5 4) inst) (_ bv1 2)) r1 ?x21))))
(let ((?x32 (ite (= ((_ extract 1 0) inst) (_ bv2 2)) (bvadd ?x23 ?x30) r2)))
?x32)))))


;r3
; 
 (let ((?x29 (ite (= ((_ extract 3 2) inst) (_ bv2 2)) r2 r3)))
(let ((?x31 (ite (= ((_ extract 3 2) inst) (_ bv0 2)) r0 (ite (= ((_ extract 3 2) inst) (_ bv1 2)) r1 ?x29))))
(let ((?x22 (ite (= ((_ extract 5 4) inst) (_ bv2 2)) r2 r3)))
(let ((?x24 (ite (= ((_ extract 5 4) inst) (_ bv0 2)) r0 (ite (= ((_ extract 5 4) inst) (_ bv1 2)) r1 ?x22))))
(let ((?x33 (ite (= ((_ extract 1 0) inst) (_ bv3 2)) (bvadd ?x24 ?x31) r3)))
?x33)))))

