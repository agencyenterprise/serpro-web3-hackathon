// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ITPFt.sol";

contract TPFt is ITPFt {
    struct TPFtUserData {
        uint256 tpfDataId;
        uint256 tpftAmount;
    }

    mapping(address => TPFtUserData[]) userTpftData;
    mapping(uint256 => TPFtData) tpfDatas;

    uint256 nextId = 0;

    function mint(
        address receiverAddress,
        uint256 tpfDataId,
        uint256 tpftAmount
    ) external {
        userTpftData[receiverAddress].push(TPFtUserData(tpfDataId, tpftAmount));
    }

    function createTPFt(TPFtData memory tpftData) external returns (uint256) {
        tpfDatas[nextId] = tpftData;
        nextId++;
        return nextId;
    }

    function getTPFtData(uint256 tpfDataId) external view returns (TPFtData memory) {
        return tpfDatas[tpfDataId];
    }

    function getUserTPFtData(address userAddress)
        external
        view
        returns (TPFtUserData[] memory)
    {
        return userTpftData[userAddress];
    }
    
}
