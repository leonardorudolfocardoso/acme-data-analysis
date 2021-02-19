import "reflect-metadata";
import {createConnection} from "typeorm";
import { Execution } from './entity/Execution';
import { Function } from './entity/Function';

createConnection().then(async connection => {

    console.log("Inserting a new Function into the database...");
    const func = new Function();
    func.functionName = "doThatThing";
    func.externalComponentAvgLatency = 0;
    func.hasExternalComponent = false;


    await connection.manager.save(func);
    console.log("Saved a new func with id: " + func.id);

    const execution = new Execution();
    execution.date = new Date('1/20/2020');
    execution.functionId = 1;
    execution.executionTime = 257;
    execution.function = func;

    await connection.manager.save(execution);
    console.log("Saved a new execution with id: " + execution.id);

    // console.log("Loading funcs from the database...");
    // const funcs = await connection.manager.find(func);
    // console.log("Loaded funcs: ", funcs);

    // console.log("Here you can setup and run express/koa/any other framework.");

}).catch(error => console.log(error));
