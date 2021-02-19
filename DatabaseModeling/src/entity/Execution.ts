import {Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn} from "typeorm";

import { Function } from './Function';

@Entity('executions')
export class Execution {

    @PrimaryGeneratedColumn()
    id: number;

    @Column('timestamp')
    date: Date;

    @Column('decimal')
    executionTime: number;

    @ManyToOne(() => Function, myfunction => myfunction.execution, { eager: true })
    @JoinColumn({ name: 'function_id'})
    function: Function; 

    @Column('decimal')
    functionId: number;

}
