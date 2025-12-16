// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ArmazemBiometria
 * @dev Contrato simples para armazenar e recuperar templates biométricos (BioCodes).
 */
contract ArmazemBiometria {
    // Array dinâmico para armazenar os biocodes em formato de bytes
    bytes[] public biocodes;

    /**
     * @dev Guarda um novo biocode na blockchain.
     * @param novoBiocode O template biométrico criptografado.
     */
    function guardarBiocode(bytes memory novoBiocode) public {
        biocodes.push(novoBiocode);
    }

    /**
     * @dev Lê um biocode específico pelo seu índice no array.
     * @param index A posição do biocode que se deseja recuperar.
     * @return O biocode em formato de bytes.
     */
    function lerBiocode(uint index) public view returns (bytes memory) {
        // Verifica se o índice é válido para evitar erros
        require(index < biocodes.length, "Indice invalido.");
        return biocodes[index];
    }

    /**
     * @dev Retorna o total de biocodes armazenados (útil para controle).
     */
    function totalBiocodes() public view returns (uint) {
        return biocodes.length;
    }
}
