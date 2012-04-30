max_h = function(vcd, N) {
    sum = 0
    for (i in 0:vcd ) { 
        comb = choose(N, i) 
        #print(paste(N, "choose", i, "=", comb))    
        sum = sum + comb 
    }
    sum
}

#original vc
omega = function(vcd, delta, N) {
    sqrt( (8/N)*log((4*max_h(vcd, 2*N))/delta) )
}

#Rademacher 
rad_omega = function(vcd, delta, N) {
    sqrt((2*log(2*N*max_h(vcd, N)))/N) + sqrt((2/N)*log(1/delta)) + 1/N
}

#Parrondo and Van den Broek, implicit function, contour graph, levels=0
pv_omega = function(vcd, delta, N, e) {
   sqrt((1/N)*(2*e + log((6*max_h(vcd, 2*N))/delta))) - e     
}

#Devroye, also implicit
d_omega = function(vcd, delta, N, e) {
    sqrt((1/(2*N))*(4*e*(1+e) + log((4*max_h(N*N))/delta))) - e
}
