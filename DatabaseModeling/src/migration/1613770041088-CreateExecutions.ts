import {MigrationInterface, QueryRunner, Table} from "typeorm";

export class CreateExecutions1613770041088 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(new Table({
            name: 'executions',
            columns: [
                {
                    name: 'id',
                    type: 'decimal',
                    isPrimary: true,
                    generationStrategy: 'increment',
                },
                
                {
                    name: 'date',
                    type: 'timestamp',
                },
                {
                    name: 'execution_time',
                    type: 'decimal',
                    precision: 5,
                },
            ],
        }));
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable('executions');
    }

}
