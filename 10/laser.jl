lines = readlines(open("input"))

for line in lines
    println(line)
end

W = length(lines[1])
H = length(lines)

most_visible = 0
best_position = nothing

coordinates = []

for x in 1:W
    for y in 1:H
        if lines[y][x] == '#'
            push!(coordinates, (x,y))
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

            count = length(above)+length(below)

            global most_visible, best_position
            if count > most_visible
                most_visible = count
                best_position = (x,y)
            end
            
        end
    end
end

function angle(p1,p2)
    xd = p1[1] - p2[1]
    yd = p1[2] - p2[2]
    d = -atan(xd,yd)
    if (d < 0) d += 2pi end
    return d
end

function distance(p1, p2)
    xd = p1[1] - p2[1]
    yd = p1[2] - p2[2]
    return sqrt(xd*xd + yd*yd)
end

function get_lt(ref)
    function my_lt(p1,p2)
        a1 = angle(ref, p1)
        a2 = angle(ref, p2)
        if !isapprox(a1,a2)
            return a1 < a2
        else 
            return distance(ref, p1) < distance(ref, p2)
        end
    end
    return my_lt
end

println(most_visible, best_position)

sort!(coordinates, lt = get_lt(best_position))

for c in coordinates
    if c != best_position
        println(c, rad2deg(angle(best_position, c)))
    end
end

filter!(p -> p != best_position, coordinates)

i = 1
count = 0
prev = nothing
prev_i = nothing 

while !isempty(coordinates) && count < 200
    global prev,count,i
    next = coordinates[i]
    if prev !== nothing
        while isapprox(angle(best_position, prev), angle(best_position, next))
            i = i + 1
            if i > length(coordinates)
                i = 1
                next = coordinates[i]
                break
            end
            next = coordinates[i]
        end
    end

    count += 1
    println("#$count ", coordinates[i], " $((coordinates[i][1] - 1)*100 + coordinates[i][2]-1)")
    deleteat!(coordinates, i)
    if (i > length(coordinates)) i = 1 end

    prev = next
end