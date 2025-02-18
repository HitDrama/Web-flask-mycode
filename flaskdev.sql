-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th1 16, 2025 lúc 04:35 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `flaskdev`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `fullname` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL,
  `phone` varchar(150) NOT NULL,
  `address` varchar(200) DEFAULT NULL,
  `image` varchar(150) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `role` varchar(150) NOT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `accounts`
--

INSERT INTO `accounts` (`id`, `fullname`, `email`, `password`, `phone`, `address`, `image`, `is_active`, `role`, `create_at`, `update_at`) VALUES
(3, 'Nguyen Van A', 'vana@gmail.com', '$2b$12$9IWHUeQn5mZTnfx.PKU5f.jiqdqFI4iC9o2iDM2PyMTYGAzZcCWZm', '02092131313', NULL, 'avatar.png', 1, 'user', '2024-10-25 13:48:59', '2024-10-25 13:48:59'),
(4, 'Nguyen Van B', 'vanb@gmail.com', '$2b$12$Tadup2aZHp1fqVPAAbpkXelI4DRG2uRXoOHwVypPHzJ7TQ1cL4LbW', '02092131313', NULL, 'avatar.png', 1, 'user', '2024-10-25 14:31:02', '2024-10-25 14:31:02'),
(5, 'Nguyen Van C', 'vanc@gmail.com', '$2b$12$UjKGqiOi5fHs3q4/V0Gllee544Vsix5W5RpSOgkQCy6xI3R1WZdu2', '12123124189', 'HCM', '1732888292_', 1, 'admin', '2024-10-25 15:20:41', '2024-11-29 20:51:32'),
(6, 'Nhanpro', '1ngay2em3lan4phat5tieng@gmail.com', '$2b$12$quvvMdwlGwrJF.Erhny53uSwGiRzpYSeBrpcFttnVAe5fZO5DZvPe', '0123456789', NULL, 'avatar.png', 1, 'user', '2024-10-30 12:47:55', '2024-10-30 20:01:48'),
(7, 'Nhân Đặng Tố', 'anhdongden15@gmail.com', '', '0123456789', NULL, 'https://lh3.googleusercontent.com/a/ACg8ocKcfVo1EOwm5zYHMhPiTnEODOOvQgdX6yDqn77BMIZQcIn3dw=s96-c', 1, 'user', '2024-10-30 15:22:00', '2024-10-30 15:22:00');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `desc` text NOT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `categories`
--

INSERT INTO `categories` (`id`, `name`, `desc`, `create_at`, `update_at`, `is_active`, `parent_id`) VALUES
(26, 'Trái cây', 'Trái cây', NULL, '2024-11-08 19:30:32', 1, NULL),
(27, 'Nước uống', 'Nước uống', NULL, '2024-11-08 19:30:54', 1, NULL),
(38, 'Rau Củ', 'Rau Củ', '2024-11-08 12:31:12', '2024-11-08 12:31:12', 1, NULL),
(39, 'Thức Ăn', 'Thức Ăn', '2024-11-08 12:31:40', '2024-11-08 12:31:40', 1, NULL);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `menus`
--

CREATE TABLE `menus` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `url` text DEFAULT NULL,
  `order` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `menus`
--

INSERT INTO `menus` (`id`, `name`, `url`, `order`, `is_active`, `parent_id`, `create_at`, `update_at`) VALUES
(1, 'Home', 'http://127.0.0.1:5000/', 1, 1, NULL, '2024-11-04 13:34:19', '2024-11-04 13:34:19'),
(2, 'Category', '/category', 2, 1, NULL, '2024-11-04 13:34:39', '2024-11-04 13:34:39'),
(3, 'Pages', '/pages', 3, 1, NULL, '2024-11-04 13:35:31', '2024-11-04 13:35:31'),
(4, 'News', '/news', 1, 1, 3, '2024-11-04 13:35:42', '2024-11-04 20:36:28'),
(5, 'Blogs', '/blogs', 2, 1, 3, '2024-11-04 13:36:05', '2024-11-04 21:27:17'),
(6, 'Contact', '/contact', 4, 1, NULL, '2024-11-04 14:43:35', '2024-11-04 14:43:35');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total_payment` float NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total_payment`, `created_at`) VALUES
(1, 5, 2242420, '2024-11-29 13:51:32');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `order_details`
--

CREATE TABLE `order_details` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float NOT NULL,
  `total` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `order_details`
--

INSERT INTO `order_details` (`id`, `order_id`, `product_name`, `quantity`, `price`, `total`) VALUES
(1, 1, 'Củ cải', 1, 1121210, 1121210),
(2, 1, 'Hành ngò', 1, 1121210, 1121210);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `desc` text NOT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `price` float NOT NULL,
  `image` varchar(150) NOT NULL,
  `category_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `products`
--

INSERT INTO `products` (`id`, `name`, `desc`, `create_at`, `update_at`, `is_active`, `price`, `image`, `category_id`) VALUES
(1, 'Chuối Chính', '<p>ưdevcwvwevdfdfbdfbdfb</p>\r\n', '2024-10-21 14:31:27', '2024-11-08 19:32:33', 1, 1121210, '1731069153_best-product-3.jpg', 26),
(12, 'Táo Tầu', 'sdgbsdbsdb', '2024-10-23 12:10:52', '2024-11-08 19:32:55', 1, 1213120, '1731069175_baner-1.png', 26),
(13, 'Dâu Tây', '<strong>D&acirc;u T&acirc;y</strong>', '2024-11-08 12:33:23', '2024-11-08 12:33:23', 1, 23242400, '1731069203_featur-2.jpg', 26),
(14, 'Táo Việt', '<strong>T&aacute;o Việt</strong>', '2024-11-08 12:33:55', '2024-11-08 12:33:55', 1, 1213120, '1731069235_best-product-6.jpg', 26),
(15, 'Nho Kẹo', '<strong>Nho Kẹo</strong>', '2024-11-08 12:34:16', '2024-11-08 12:34:16', 1, 23242400, '1731069256_fruite-item-5.jpg', 26),
(16, 'Nho Mẫu Đơn', '<strong>Nho Mẫu Đơn</strong>', '2024-11-08 12:34:47', '2024-11-08 12:34:47', 1, 1213120, '1731069287_best-product-5.jpg', 26),
(17, 'Cam cúng', 'Cam c&uacute;ng', '2024-11-08 12:35:32', '2024-11-08 12:35:32', 1, 1121210, '1731069332_fruite-item-1.jpg', 26),
(18, 'Trái cây gần hư', 'Tr&aacute;i c&acirc;y gần hư', '2024-11-08 12:35:59', '2024-11-08 12:35:59', 1, 12500000, '1731069359_hero-img-1.png', 26),
(19, 'Sting Dừa', 'Sting Dừa', '2024-11-08 12:36:35', '2024-11-08 12:36:35', 1, 1213120, '1731069395_vegetable-item-2.jpg', 27),
(20, 'Coca trứng', 'Coca trứng', '2024-11-08 12:36:59', '2024-11-08 12:36:59', 1, 1121210, '1731069419_testimonial-1.jpg', 27),
(21, 'Sinh tố sầu riêng', 'Sinh tố sầu ri&ecirc;ng', '2024-11-08 12:37:49', '2024-11-08 12:37:49', 1, 23242400, '1731069469_fruite-item-2.jpg', 27),
(22, 'Trà sữa ruốc', 'Tr&agrave; sữa ruốc', '2024-11-08 12:38:19', '2024-11-08 12:38:19', 1, 1213120, '1731069499_hero-img-2.jpg', 27),
(23, 'Pepsi hành', '<em>Pepsi h&agrave;nh</em>', '2024-11-08 12:38:58', '2024-11-08 12:38:58', 1, 1121210, '1731069538_vegetable-item-1.jpg', 27),
(24, 'Củ cải', 'Củ cải', '2024-11-08 12:39:57', '2024-11-08 12:39:57', 1, 1121210, '1731069597_single-item.jpg', 38),
(25, 'Hành ngò', '<em><strong>H&agrave;nh ng&ograve;</strong></em>', '2024-11-08 12:40:15', '2024-11-08 12:40:15', 1, 1121210, '1731069615_vegetable-item-6.jpg', 38),
(26, 'Cà chua', '<strong>C&agrave; chua</strong>', '2024-11-08 12:40:45', '2024-11-08 12:40:45', 1, 1121210, '1731069645_vegetable-item-1.jpg', 38);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Chỉ mục cho bảng `menus`
--
ALTER TABLE `menus`
  ADD PRIMARY KEY (`id`),
  ADD KEY `parent_id` (`parent_id`);

--
-- Chỉ mục cho bảng `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Chỉ mục cho bảng `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT cho bảng `menus`
--
ALTER TABLE `menus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT cho bảng `order_details`
--
ALTER TABLE `order_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`);

--
-- Các ràng buộc cho bảng `menus`
--
ALTER TABLE `menus`
  ADD CONSTRAINT `menus_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `menus` (`id`);

--
-- Các ràng buộc cho bảng `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`id`);

--
-- Các ràng buộc cho bảng `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

--
-- Các ràng buộc cho bảng `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
