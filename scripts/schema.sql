CREATE TABLE `code_conversions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键，自增',
    `user_id` VARCHAR(36) NOT NULL COMMENT '用户唯一标识',
    `input_code` TEXT NOT NULL COMMENT '输入的代码',
    `target_language` VARCHAR(50) NOT NULL COMMENT '目标语言',
    `output_code` TEXT NOT NULL COMMENT '转换后的代码',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL COMMENT '修改时间',
    INDEX `idx_code_conversions_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='代码转换记录表';