X_flat = map(c->parse(Int, c), collect(readline(open("input"))))

W=25
H=6
n = length(X_flat) ÷ (W*H)

X_layers = reshape(X_flat, W*H, n)

min_zeros = W*H
min_i = -1

for i in 1:size(X_layers)[2]
    global min_zeros
    global min_i
    
    layer = X_layers[:,i]
    zeros = sum(layer .== 0)
    
    if (zeros < min_zeros)
        min_zeros = zeros
        min_i = i
    end
end

layer = X_layers[:,min_i]
ones = sum(layer .== 1)
twos = sum(layer .== 2)

println(ones * twos)

layer_sum = X_layers[:,1][:]

for i in 1:size(X_layers)[2]
    global layer_sum
    layer = X_layers[:,i]
    for j in 1:length(layer)
        if layer_sum[j] == 2
            layer_sum[j] = layer[j]
        end
    end
end

println(reshape(layer_sum,W,H)')