function main() 
    grid = collect.(readlines(open("input")))

    grids = Dict()
    grids[0] = grid

    flatten(A) = join(join.(A))
    bugcount(A) = length([i for i in 1:25 if flatten(A)[i] == '#'])
    emptygrid() = [['.' for i in 1:5] for j in 1:5]

    function adjacents(x, y, level)
        adj = []
        if y > 1 && !(x == 3 && y == 4)
            push!(adj, grids[level][y-1][x])
        elseif x == 3 && y == 4
            for i in 1:5
                push!(adj, grids[level+1][5][i])
            end
        elseif y == 1
            push!(adj, grids[level-1][2][3])
        end

        if x > 1 && !(x == 4 && y == 3)
            push!(adj, grids[level][y][x-1])
        elseif x == 4 && y == 3
            for i in 1:5
                push!(adj, grids[level+1][i][5])
            end
        elseif x == 1
            push!(adj, grids[level-1][3][2])
        end

        if x < 5 && !(x == 2 && y == 3)
            push!(adj, grids[level][y][x+1])
        elseif x == 2 && y == 3
            for i in 1:5
                push!(adj, grids[level+1][i][1])
            end
        elseif x == 5
            push!(adj, grids[level-1][3][4])
        end

        if y < 5 && !(x == 3 && y == 2)
            push!(adj, grids[level][y+1][x])
        elseif x == 3 && y == 2
            for i in 1:5
                push!(adj, grids[level+1][1][i])
            end
        elseif y == 5
            push!(adj, grids[level-1][4][3])
        end

        return adj
    end

    function next_state(grid, level)
        next_grid = deepcopy(grid)

        for y in 1:5
            for x in 1:5
                if y == 3 && x == 3 
                    continue
                end
                adj = adjacents(x, y, level)
                bugs = count(c->c=='#', adj)
                if grid[y][x] == '#'
                    if bugs != 1
                        next_grid[y][x] = '.'
                    else
                        next_grid[y][x] = '#'
                    end
                else #  '.'
                    if bugs < 1 || bugs > 2
                        next_grid[y][x] = '.'
                    else
                        next_grid[y][x] = '#'
                    end
                end
            end
        end
        return next_grid
    end

    for i in 1:201
        grids[i] = emptygrid()
        grids[-i] = emptygrid()
    end

    n_iters = 200

    for i in 1:n_iters
        newgrids = Dict()

        for j in -i:i
            newgrids[j] = next_state(grids[j], j)
        end

        for j in -i:i
            grids[j] = newgrids[j]
        end

        println("======")
        for i in -1:1
            println.(join.(grids[i]))
            println()
        end
    end

    println("Bugs: ",sum(bugcount.(values(grids))))
    
end

main()