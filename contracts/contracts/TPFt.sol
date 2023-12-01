// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ITPFt.sol";


contract TPFt is ITPFt {
    struct TPFtUserData {
        uint256 tpfDataId;
        uint256 tpftAmount;
    }

    mapping(address => TPFtUserData[]) name;
    mapping(uint256 => TPFtData) tpfDatas;

    //counter with next available id
    uint256 nextId = 0;

    function mint(
        address receiverAddress,
        uint256 tpfDataId,
        uint256 tpftAmount
    ) external {
        name[receiverAddress].push(TPFtUserData(tpfDataId, tpftAmount));
    }

    function createTPFt(TPFtData memory tpftData) external returns (uint256) {
        tpfDatas[nextId] = tpftData;
        nextId++;
        return nextId;
    }
}
