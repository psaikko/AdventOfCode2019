lines = readlines(open("input"))
lines = filter(s -> !isempty(s), lines)
masses = map(s -> parse(Int, s), lines)
function fuel(mass)
    fm = mass ÷ 3 - 2
    if (fm <= 0) return 0 end
    return fm + fuel(fm)
end
fuels = map(fuel, masses)
println(sum(fuels))
