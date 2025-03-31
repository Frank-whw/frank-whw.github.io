# Proj1
## **1. PPM 图像格式详解**
- **基本概念**
  - **PPM (Portable Pixmap)**：一种无损的位图图像格式，属于 Netpbm 格式家族
  - **两种编码形式**：
    | 类型 | 标识头 | 存储方式 | 特点 |
    |---|---|---|---|
    | ASCII | `P3` | 纯文本存储 RGB 值 | 可读性强，文件体积大 |
    | Binary | `P6` | 二进制存储像素数据 | 文件小，不可直接阅读 |

- **文件结构示例**：
  ```ppm
  P3                  # 格式标识
  4 4                 # 宽度(4像素) 高度(4像素)
  255                 # 颜色最大值（通常为255）
  255 0 0  0 255 0    # 像素数据（R G B 值）
  0 0 255  255 255 0  # 每行建议不超过70字符
  ```

- **内存布局**
  ```c
  typedef struct {
      uint8_t R, G, B; // 每个通道占1字节（0-255）
  } Color;
  
  typedef struct {
      int rows, cols;
      Color **image;   // 二维数组，rows行，cols列
  } Image;
  ```

---

## **2. 代码分析与改进**

### **imageloader.c 关键点**
- **内存分配修正**
  ```c
  // 错误写法（分配指针数组）
  img->image[row] = malloc(sizeof(Color*) * cols);
  
  // 正确写法（分配结构体数组）
  img->image[row] = malloc(sizeof(Color) * cols);
  ```
  - 每个 `image[row]` 应指向 `Color` 结构体数组，而非指针数组

- **错误处理增强**
  ```c
  FILE *fp = fopen(filename, "r");
  if (!fp) {
      perror("Error opening file");
      return NULL;
  }
  
  // 读取时检查返回值
  if (fscanf(fp, "%d %d", &cols, &rows) != 2) {
      fprintf(stderr, "Invalid image dimensions");
      fclose(fp);
      return NULL;
  }
  ```

- **跳过注释的实现**
  ```c
  int ch;
  while ((ch = fgetc(fp)) == '#') { 
      while ((ch = fgetc(fp)) != '\n'); // 跳过注释行
  }
  ungetc(ch, fp); // 回退非注释字符
  ```

---

## **3. 隐写术 (Steganography) 实现**
- **核心逻辑**
  ```c
  Color* evaluateOnePixel(Image *image, int row, int col) {
      Color *c = malloc(sizeof(Color));
      if (!c) return NULL;
      
      // 提取 B 通道最低有效位（LSB）
      uint8_t lsb = image->image[row][col].B & 0x1;
      c->R = c->G = c->B = (lsb ? 255 : 0);
      return c;
  }
  ```
  - **关键技巧**：`& 0x1` 操作快速获取最后一位
  - **内存安全**：每次分配后检查指针有效性

---

## **4. 康威生命游戏 (Game of Life)**
- **规则说明**
  - 活细胞（白色像素）存活条件：2-3个活邻居
  - 死细胞（黑色像素）复活条件：恰好3个活邻居
  - 使用环形边界（Toroidal Boundary）处理边缘

- **邻居计数函数**
  ```c
  int countLiveNeighbors(Image *img, int row, int col) {
      int count = 0;
      for (int i = -1; i <= 1; i++) {
          for (int j = -1; j <= 1; j++) {
              if (i == 0 && j == 0) continue;
              
              int r = (row + i + img->rows) % img->rows;
              int c = (col + j + img->cols) % img->cols;
              
              if (img->image[r][c].B & 1) count++;
          }
      }
      return count;
  }
  ```

---

## **5. 常见错误与调试技巧**
- **内存错误排查**
  ```bash
  # 使用 Valgrind 检测内存泄漏
  valgrind --leak-check=full ./steganography input.ppm
  ```

- **二维数组访问的正确方式**
  ```c
  // 正确访问方式（结构体数组）
  Color pixel = image->image[row][col];
  
  // 错误访问方式（若错误分配为指针数组）
  Color *pixel = image->image[row][col]; // 导致段错误
  ```

---

## **6. 项目总结**
- **关键知识点**
  - 二进制文件与文本文件的区别
  - 位操作的实际应用（LSB 提取）
  - 动态内存管理的正确实践
  - 模块化编程思想（imageloader 模块解耦）

- **延伸思考**
  - 如何改进 PPM 的存储效率？
  - 多线程图像处理的潜在优化方向
  - 其他图像隐写术方法（如 LSB 替换算法）
---
## 7. **代码**

- imageloader.c
```c
/************************************************************************
**
** NAME:        imageloader.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**              Justin Yokota - Starter Code
**				Frank
**
**
** DATE:        2025-03-31
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "imageloader.h"

// Opens a .ppm P3 image file, and constructs an Image object.
// You may find the function fscanf useful.
// Make sure that you close the file with fclose before returning.
Image *readData(char *filename)
{
	// YOUR CODE HERE
	FILE *fp = fopen(filename, "r");
	Image *img = malloc(sizeof(Image));
	char format[4];
	fscanf(fp, "%s", format);
	fscanf(fp, "%d %d", &img->cols, &img->rows);
	img->image = malloc(sizeof(Color **) * img->rows);
	int nums;
	fscanf(fp, "%d", &nums);
	for (int row = 0; row < img->rows; row++)
	{
		img->image[row] = malloc(sizeof(Color *) * img->cols);
		for (int col = 0; col < img->cols; col++)
		{
			// printf("%d\n", row);
			fscanf(fp, "%hhu %hhu %hhu", &img->image[row][col].R, &img->image[row][col].G, &img->image[row][col].B);
		}
	}
	fclose(fp);
	return img;
}

// Given an image, prints to stdout (e.g. with printf) a .ppm P3 file with the image's data.
void writeData(Image *image)
{
	// YOUR CODE HERE
	printf("P3\n%d %d\n255\n", image->cols, image->rows);
	for (int row = 0; row < image->rows; row++)
	{
		for (int col = 0; col < image->cols; col++)
		{
			if (col != 0)
				printf("   ");
			printf("%3hhu %3hhu %3hhu", image->image[row][col].R, image->image[row][col].G, image->image[row][col].B);
		}
		printf("\n");
	}
}

// Frees an image
void freeImage(Image *image)
{
	// YOUR CODE HERE
	for (int row = 0; row < image->rows; row++)
	{
		free(image->image[row]);
	}
	free(image->image);
	free(image);
}

// int main()
// {
// 	Image *img = readData("JohnConway.ppm");
// 	writeData(img);
// }
```

- steganography.c
```c
/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				Frank
**
** DATE:        2025-03-31
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

// Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	// YOUR CODE HERE
	Color *color = malloc(sizeof(Color));
	if (image->image[row][col].B & 1)
	{
		// the last bits of B is 1, means the color should be black
		color->R = 255;
		color->G = 255;
		color->B = 255;
	}
	else
	{
		color->R = 0;
		color->G = 0;
		color->B = 0;
	}
	return color;
}

// Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	// YOUR CODE HERE
	Image *newImage = malloc(sizeof(Image));
	newImage->rows = image->rows;
	newImage->cols = image->cols;
	newImage->image = malloc(sizeof(Color **) * image->rows);
	for (int row = 0; row < image->rows; row++)
	{
		newImage->image[row] = malloc(sizeof(Color *) * image->cols);
		for (int col = 0; col < image->cols; col++)
		{
			newImage->image[row][col] = *evaluateOnePixel(image, row, col);
		}
	}
	return newImage;
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image,
where each pixel is black if the LSB of the B channel is 0,
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/

// #include "imageloader.c"
// It seems I don'tmake  need to include this c problem, because in the imageloader.h there are extern functions.
int main(int argc, char **argv)
{
	// YOUR CODE HERE
	char *filename = argv[1];
	Image *img = readData(filename);
	Image *newImg = steganography(img);
	writeData(newImg);

	freeImage(img);
	freeImage(newImg);
}

```

- gameoflife.c
```c
/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				Frank
**
** DATE:        2025-03-31
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

// Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	// YOUR CODE HERE
	Color *color = malloc(sizeof(Color));
	if (image->image[row][col].B & 1)
	{
		// the last bits of B is 1, means the color should be black
		color->R = 255;
		color->G = 255;
		color->B = 255;
	}
	else
	{
		color->R = 0;
		color->G = 0;
		color->B = 0;
	}
	return color;
}

// Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	// YOUR CODE HERE
	Image *newImage = malloc(sizeof(Image));
	newImage->rows = image->rows;
	newImage->cols = image->cols;
	newImage->image = malloc(sizeof(Color **) * image->rows);
	for (int row = 0; row < image->rows; row++)
	{
		newImage->image[row] = malloc(sizeof(Color *) * image->cols);
		for (int col = 0; col < image->cols; col++)
		{
			newImage->image[row][col] = *evaluateOnePixel(image, row, col);
		}
	}
	return newImage;
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image,
where each pixel is black if the LSB of the B channel is 0,
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/

// #include "imageloader.c"
// It seems I don'tmake  need to include this c problem, because in the imageloader.h there are extern functions.
int main(int argc, char **argv)
{
	// YOUR CODE HERE
	char *filename = argv[1];
	Image *img = readData(filename);
	Image *newImg = steganography(img);
	writeData(newImg);

	freeImage(img);
	freeImage(newImg);
}

```