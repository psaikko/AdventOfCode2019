function main()
    technique_strings = readlines(open("input"))
    n = 119315717514047

    mult::BigInt = 1
    shift::BigInt = 0

    function cut(k)
        shift = (shift + k) % n
    end

    function deal_with_increment(i)
        mult = (mult * i) % n
        shift = (shift * i) % n
    end

    for s in technique_strings
        if s == "deal into new stack"
            # Decompose into deal with increment and cut
            deal_with_increment(n-1)
            cut(1)
        elseif startswith(s, "deal with")
            i = parse(Int, split(s)[end])
            deal_with_increment(i)
        elseif startswith(s, "cut")
            # Convert negative cuts to positive
            k = parse(Int, split(s)[end])
            if (k < 0) k += n end
            cut(k)
        end
    end

    # Input is equivalent to 
    # deal with increment $mult
    # cut $shift
    a::BigInt = mult
    b::BigInt = shift
    inv::BigInt = invmod(a, n)

    # Final position of card x is given by
    # Linear congruence ax + b (mod n)
    f(x) = (((x * a) % n) + n - b) % n
    f_inv(y) = (((y + b) % n) * inv) % n

    
    reps = 101741582076661
    # Repeating f $reps times is essentially
    # running a linear congruential generator.
    # We precompute the values of a and b 
    # for appluing f 2^i times
    fvals = [(a,b)]
    for i in 1:100
        pa, pb = fvals[end]
        push!(fvals, ((pa*pa)%n, (((pa+1)*pb) % n)))
    end

    # And similarly for the inverse of f
    # g(y) = (y + b) * inv = y*inv + b*inv
    # g(g(y)) = (y*inv*inv + b*(inv*inv + inv))
    # ...
    finv_vals = [(inv,(b*inv) % n)]
    for i in 1:100
        pa, pb = finv_vals[end]
        push!(finv_vals, ((pa*pa)%n, (((pa+1)*pb) % n)))
    end

    # This gives a fast way of computing f^p(x) for p power of 2
    # compute f^(2^p) (x)
    fpow_fast2(x, p) = (((x * fvals[p+1][1]) % n) + n - fvals[p+1][2]) % n
    # compute f^p (x)
    fpow_slow(x, p) = p == 1 ? f(x) : f(fpow_slow(x, p - 1))

    # compute f^(2^p) (x)
    finv_pow_fast2(x, p) = (((x * finv_vals[p+1][1]) % n) + finv_vals[p+1][2]) % n
    # compute f^p (x)
    finv_pow_slow(x, p) = p == 1 ? f_inv(x) : f_inv(finv_pow_slow(x, p - 1))

    # Sanity checks
    # println("fast")
    # println(finv_pow_fast2(1,0))
    # println(finv_pow_fast2(1,1))
    # println(finv_pow_fast2(1,2))
    # println(finv_pow_fast2(1,3))

    # println("slow")
    # println(finv_pow_slow(1,1))
    # println(finv_pow_slow(1,2))
    # println(finv_pow_slow(1,4))
    # println(finv_pow_slow(1,8))

    # Decompose p to sum of powers of 2 to compute f^p(x) for arbitrary p
    function fpow_fast(x,p)
        for p2 in reverse(collect(0:62))
            if 2^p2 <= p
                p -= 2^p2
                x = fpow_fast2(x, p2)
            end
        end
        return x
    end

    function finv_pow_fast(y,p)
        for p2 in reverse(collect(0:62))
            if 2^p2 <= p
                p -= 2^p2
                y = finv_pow_fast2(y, p2)
            end
        end
        return y
    end

    # Sanity checks
    # println("fast")
    # for i in 1:10
    #     println(finv_pow_fast(1,i))
    # end

    # println("slow")
    # for i in 1:10
    #     println(finv_pow_slow(1,i))
    # end

    println(finv_pow_fast(2020, reps))
end

main()