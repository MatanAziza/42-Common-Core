/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libftprintf.h                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 14:14:31 by maziza            #+#    #+#             */
/*   Updated: 2025/11/10 14:18:04 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <stdlib.h>
# include <unistd.h>

int	ft_putchar(int fd, char c);
int	ft_strlen(char *str);
int	ft_putstr(int fd, char *s);
int	ft_putnbr_base(int fd, long int nb, const char *base, int sign);
int	ft_print_address(int fd, unsigned long address, const char *base);
int	ft_check_flag(char c);
int	ft_printf(int fd, const char *flag, ...);
int	ft_putnbr_address(int fd, unsigned long nbr, const char *base);

#endif
