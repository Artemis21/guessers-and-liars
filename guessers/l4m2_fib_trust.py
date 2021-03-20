def Main(rng, liar):
    times=[8]*256
    weight=[1,2,3,5,8,13,21,34,55]
    while 1:
        a=[i>=0 and weight[i] for i in times]
        b=(sum(a)+1)/2
        guess=-1
        #print(times)
        while b>0:
            guess=guess+1
            b=b-a[guess]
        cmp=liar(guess)
        times=[times[i]-(i==guess or (cmp<0)^(i<guess)) for i in range(256)]
