function main()
    technique_strings = readlines(open("input"))

    function cut(stack, k)
        if k > 0
            first, rest = stack[1:k], stack[k+1:end]
            push!(rest, first...)
            return rest
        else
            k = abs(k)
            first, rest = stack[1:end-(k)], stack[end-(k-1):end]
            push!(rest, first...)
            return rest
        end
    end

    function deal_into_new(stack)
        return reverse(stack)
    end

    function deal_with_increment(stack, i)
        newstack = zeros(Int, size(stack))

        j = 1
        for v in stack
            newstack[j] = v
            j += i 
            if j > length(stack)
                j -= length(stack)
            end
        end

        return newstack
    end

    technique_functions = []

    for s in technique_strings
        if s == "deal into new stack"
            push!(technique_functions, deal_into_new)
        elseif startswith(s, "deal with")
            i = parse(Int, split(s)[end])
            push!(technique_functions, s -> deal_with_increment(s, i))
        elseif startswith(s, "cut")
            k = parse(Int, split(s)[end])
            push!(technique_functions, s -> cut(s, k))
        else
            println(s)
            exit()
        end
    end

    stack = collect(0:10006)

    for f in technique_functions
        stack = f(stack)
        #println(stack)
    end

    println(indexin(2019, stack))
end

main()