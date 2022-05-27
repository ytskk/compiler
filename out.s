.data
.text

main:
addi $sp, $sp, -8
sw $ra, 0($sp)
lui $1, 15107
mtc1 $1, $f4
lw $t0, 4($sp)
add $a0 $zero, $t0
jal getEulerNumber
add $a0 $zero, $v0
jal print
lw $ra, 0($sp)
addi $sp, $sp, 8
li $v0 10 #program finished call terminate
syscall

factorial:
addi $sp, $sp, -16
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $a0, 4($sp)
li $t0,1
sw $t0, 8($sp)
li $t0,1
sw $t0, 12($sp)
lbl2:
lw $t0, 8($sp)
lw $t1, 4($sp)
bgt $t0, $t1, lbl1
lw $t0, 12($sp)
lw $t1, 8($sp)
mul $t2, $t0, $t1
sw $t2, 12($sp)
lw $t0, 8($sp)
addi $t0, $t0, 1
sw $t0, 8($sp)
j lbl2
lbl1:
lw $t0, 12($sp)
add $v0, $zero, $t0
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra

getEulerNumber:
addi $sp, $sp, -20
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $a0, 4($sp)
lui $1, 0
mtc1 $1, $f4
li $t0,0
sw $t0, 12($sp)
lui $1, 16256
mtc1 $1, $f4
lbl4:
lw $t0, 16($sp)
lw $t1, 4($sp)
ble $t0, $t1, lbl3
lw $t0, 12($sp)
add $a0 $zero, $t0
jal factorial
li $t1,1
div $t0, $t1, $v0
sw $t0, 16($sp)
lw $t0, 8($sp)
lw $t1, 16($sp)
add $t2, $t0, $t1
sw $t2, 8($sp)
lw $t0, 12($sp)
addi $t0, $t0, 1
sw $t0, 12($sp)
j lbl4
lbl3:
lw $t0, 8($sp)
add $v0, $zero, $t0
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
