lines = readlines(open("input"))

println(lines)

W = length(lines[1])
H = length(lines)

m = 0

for x in 1:W
    for y in 1:H
        if lines[y][x] == '#'
            above = Set()
            below = Set()
            for x2 in 1:W
                for y2 in 1:H
                    if lines[y2][x2] == '#' && (x,y) != (x2,y2)
                        xd = x - x2
                        yd = y - y2
                        if yd >= 0
                            push!(above, xd//yd)
                        else 
                            push!(below, xd//yd)
                        end            
                    end
                end
            end
            println((x-1,y-1),length(above)+length(below))

            global m
            m = max(m, length(above)+length(below))
        end
    end
end

println(m)