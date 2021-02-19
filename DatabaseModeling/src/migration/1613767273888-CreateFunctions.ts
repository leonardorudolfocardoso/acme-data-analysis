import {MigrationInterface, QueryRunner, Table} from "typeorm";

export class CreateFunctions1613767273888 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(new Table({
            name: 'functions',
            columns: [
                {
                    name: 'id',
                    type: 'decimal',
                    isPrimary: true,
                    generationStrategy: 'increment',
                },
                {
                    name: 'function_name',
                    type: 'varchar',
                },
                {
                    name: 'external_component_avg_latency',
                    type: 'decimal',
                    precision: 5,
                },
                {
                    name: 'has_external_component',
                    type: 'boolean',
                },
            ],
        }));
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable('functions');
    }

}
