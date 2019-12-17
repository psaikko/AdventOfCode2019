import Base.Threads

println(Threads.nthreads())

function main()
    line = readline(open("input"))

    println(line)

    numbers = map(c->parse(Int, c), collect(line))

    let signal = repeat(numbers, 10000)
        n = length(signal)
        for phase in 1:100

            println(phase)
            transformed = zeros(Int,size(signal))

            sums = accumulate(+, signal)

            function get_sum(a,b)
                as = a > 1 ? sums[a-1] : 0
                return sums[min(b,end)] - as
            end

            Threads.@threads for i in 1:n

                start_ind = i
                val = 0

                while start_ind <= n
                    val += get_sum(start_ind, start_ind + i - 1)
                    start_ind += 4i
                end

                start_ind = 3i

                while start_ind <= n
                    val -= get_sum(start_ind, start_ind + i - 1)
                    start_ind += 4i
                end

                transformed[i] = abs(val) % 10
            end

            signal[:] = transformed
        end

        to_int(l) = parse(Int,join(string.(l)))

        offset = to_int(numbers[1:7])
        println(offset)

        ans = to_int(signal[offset+1:offset+8])
        println(ans)
    end
end

@time main()