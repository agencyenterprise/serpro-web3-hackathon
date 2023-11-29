pragma circom 2.0.0;

include "../node_modules/circomlib-ml/circuits/ArgMax.circom";
include "../node_modules/circomlib-ml/circuits/Dense.circom";

template Model() {
signal input in[200];
signal input dense_2_weights[200][2];
signal input dense_2_bias[2];
signal output out[1];

component dense_2 = Dense(200, 2);
component dense_2_softmax = ArgMax(2);

for (var i0 = 0; i0 < 200; i0++) {
    dense_2.in[i0] <== in[i0];
}
for (var i0 = 0; i0 < 200; i0++) {
    for (var i1 = 0; i1 < 2; i1++) {
        dense_2.weights[i0][i1] <== dense_2_weights[i0][i1];
}}
for (var i0 = 0; i0 < 2; i0++) {
    dense_2.bias[i0] <== dense_2_bias[i0];
}
for (var i0 = 0; i0 < 2; i0++) {
    dense_2_softmax.in[i0] <== dense_2.out[i0];
}
out[0] <== dense_2_softmax.out;

}

component main = Model();
