pragma solidity ^0.8.19;

interface ITPFt {
        
    struct TPFtData {
        string acronym;
        string code;
        uint256 maturityDate;
    }

  function createTPFt ( TPFtData memory tpftData ) external returns ( uint256 );
  function mint ( address receiverAddress, uint256 tpfDataId, uint256 tpftAmount ) external;

  // function allowAuctionPlacement ( address member ) external;
  // function allowDirectPlacement ( address member ) external;
  // function allowFreezingPlacement ( address member ) external;
  // function allowTPFtMint ( address member ) external;
  // function decreaseFrozenBalance ( address from, TPFtData memory tpftData, uint256 tpftAmount ) external;
  // function directPlacement ( address from, address to, TPFtData memory tpftData, uint256 tpftAmount ) external;
  // function disableAddress ( address member ) external;
  // function enableAddress ( address member ) external;
  // function getRoleAdmin ( bytes32 role ) external view returns ( bytes32 );
  // function getTPFtId ( TPFtData memory tpftData ) external view returns ( uint256 );
  // function grantRole ( bytes32 role, address account ) external;
  // function hasRole ( bytes32 role, address account ) external view returns ( bool );
  // function increaseFrozenBalance ( address from, TPFtData memory tpftData, uint256 tpftAmount ) external;
  // function isEnabledAddress ( address member ) external returns ( bool isEnabled );
  // function pause (  ) external;
  // function renounceRole ( bytes32 role, address account ) external;
  // function revokeRole ( bytes32 role, address account ) external;
  // function unpause (  ) external;
}

