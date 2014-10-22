'''
Created on Aug 28, 2014

@author: michal
'''
import module1, module2
module1.func()
print '\t---module2---'

M = module2.M
mem2 = module2.M.member2
module2.M.clear()
print '====';print M.member2; print mem2
module2.M.set_mem2()
print '====';print M.member2; print mem2
M.set_mem2()
print '====';print M.member2; print mem2
M.clear()
print '====';print M.member2; print mem2
module1.func()


print '\n\n====';print M.member2; print mem2