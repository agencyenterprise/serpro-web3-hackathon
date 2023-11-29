// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ITPFt.sol";


struct TPFtUserData {
    string acronym;
    string code;
    uint256 maturityDate;
}
contract TPFt is ITPFt {
        
    mapping (address => TPFtData[]) name;
    mapping (uint256 => TPFtData) tpfDatas;

    //counter with next available id
    uint256 nextId = 0;
    
    function mint ( address receiverAddress, uint256 tpfDataId, uint256 tpftAmount ) external {
    name[receiverAddress].push(tpftData);
    }

    function createTPFt ( TPFtData memory tpftData ) external returns ( uint256 ) {
        tpfDatas[nextId] = tpftData;
        nextId++;
        return nextId;
    }
}
