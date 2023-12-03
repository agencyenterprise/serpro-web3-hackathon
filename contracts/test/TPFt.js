const { expect } = require("chai");
const { ethers } = require("hardhat");
require("@nomicfoundation/hardhat-ethers");

describe("TPFt contract", function () {
  let contractDeployed;

  beforeEach(async () => {
    contractDeployed = await ethers.deployContract("TPFt");
  });

  it("Should add tpf data", async function () {
    const tpftData = {
      acronym: "Test",
      code: "TST",
      maturityDate: new Date().getTime(),
    };
    const createTPFtResponse = await contractDeployed.createTPFt(tpftData);
    await createTPFtResponse.wait();
    await expect(await contractDeployed.getTPFtData(0)).deep.equal([
      tpftData.acronym,
      tpftData.code,
      tpftData.maturityDate,
    ]);
  });
  
  it("Should mint tpf data", async function () {
    const [owner, addr1, addr2] = await ethers.getSigners();
    const tpftData = {
      acronym: "Test",
      code: "TST",
      maturityDate: new Date().getTime(),
    };
    const createTPFtResponse = await contractDeployed.createTPFt(tpftData);
    await createTPFtResponse.wait();

    const mintTPFtResponse = await contractDeployed.mint(addr1, 0, 100);
    await mintTPFtResponse.wait();

    const mint2TPFtResponse = await contractDeployed.mint(addr1, 0, 50);
    await mint2TPFtResponse.wait();

    await expect(await contractDeployed.getUserTPFtData(addr1)).deep.equal([
      [0n, 100n],
      [0n, 50n],
    ]);

    const mint3TPFtResponse = await contractDeployed.mint(addr2, 0, 50);
    await mint3TPFtResponse.wait();

    await expect(await contractDeployed.getUserTPFtData(addr2)).deep.equal([
      [0n, 50n],
    ]);
  });
});
