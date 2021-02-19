import {MigrationInterface, QueryRunner, TableColumn, TableForeignKey} from "typeorm";

export class AddFunctionIdToExecutions1613770228986 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.addColumn(
            'executions',
            new TableColumn({
                name: 'function_id',
                type: 'decimal',
                isNullable: true
            })
        );

        await queryRunner.createForeignKey(
            'executions',
            new TableForeignKey({
                columnNames: ['function_id'],
                referencedColumnNames: ['id'],
                referencedTableName: 'functions',
                name: 'FunctionId',
                onUpdate: 'CASCADE',
                onDelete: 'SET NULL'
            })
        );
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropForeignKey('executions', 'FunctionId');

        await queryRunner.dropColumn('executions', 'function_id');
    }

}
