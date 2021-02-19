import {Entity, PrimaryGeneratedColumn, Column, OneToMany} from "typeorm";

import { Execution } from './Execution';

@Entity('functions')
export class Function {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    functionName: string;

    @Column('decimal')
    externalComponentAvgLatency: number;

    @Column('boolean')
    hasExternalComponent: boolean;

    @OneToMany(() => Execution, execution => execution.functionId)
    execution: Execution

}
