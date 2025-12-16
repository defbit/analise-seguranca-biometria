// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ArmazemBiometria {
    bytes[] public biocodes;

    function guardarBiocode(bytes memory novoBiocode) public {
        biocodes.push(novoBiocode);
    }

    // Função de leitura simplificada: lê um item pelo seu índice (posição)
    function lerBiocode(uint index) public view returns (bytes memory) {
        return biocodes[index];
    }
}