/* skel-layers.js v1.0.3 | (c) n33 | getskel.com | MIT licensed 
	simple mod in nav case
*/

skel.registerPlugin('layers', (function($) {

	// No jQuery? Bail.
		if (typeof $ == 'undefined')
			return false;

	/**************************************************************************/
	/* jQuery Functions                                                       */
	/**************************************************************************/

		/**
		 * Demotes the element back to its previous z-index value.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_demote = function() {

			if (this.length > 1) {
			
				for (var i=0; i < this.length; i++)
					$(this[i])._skel_layers_demote();
					
				return $(this);

			}

			var t = $(this);
			
			t
				.css('z-index', t.data('skel-layers-layer-z-index'))
				.data('skel-layers-layer-z-index', '');
			
			return t;
		
		};
		
		/**
		 * Expands the grid cell to fill any remaining space in its row.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_expandCell = function() {
			
			var	t = $(this),
				p = t.parent(),
				diff = 12;
			
			p.children().each(function() {
				
				var	t = $(this),
					c = t.attr('class');
				
				if (c && c.match(/(\s+|^)([0-9]+)u(\s+|$)/))
					diff -= parseInt(RegExp.$2);
			
			});
			
			if (diff > 0) {
				
				t._skel_layers_initializeCell();
				t.css('width', (((t.data('cell-size') + diff) / 12) * 100.00) + '%');
			
			}
		
		};

		/**
		 * Determines if the element has at least one parent.
		 * @return {bool} If true, element has a parent. If false, element does not have a parent.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_hasParent = function() {
			return ($(this).parents().length > 0);
		};
		
		/**
		 * Prepares the grid cell for use with actions.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_initializeCell = function() {
			
			var t = $(this);
			
			if (t.attr('class').match(/(\s+|^)([0-9]+)u(\s+|$)/))
				t.data('cell-size', parseInt(RegExp.$2));
		
		};

		/**
		 * Promotes the element to a given z-index (based on the global base z-index).
		 * @param {integer} n Optional z-index (if omitted, defaults to 1).
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_promote = function(n) {

			if (this.length > 1) {
			
				for (var i=0; i < this.length; i++)
					$(this[i])._skel_layers_promote(n);
					
				return $(this);

			}

			var t = $(this), x;

			if (isNaN(x = parseInt(t.data('skel-layers-layer-index'))))
				x = 0;

			t
				.data('skel-layers-layer-z-index', t.css('z-index'))
				.css('z-index', _.config.baseZIndex + x + (n ? n : 1));
			
			return t;

		};
		
		/**
		 * Resets all forms within the element.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_resetForms = function() {
		
			var t = $(this);
			
			$(this).find('form').each(function() {
				this.reset();
			});
			
			return t;
		
		};
		
		/**
		 * Does a cross-browser css() call (property and value).
		 * @param {string} p Property.
		 * @param {string} v Value.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_xcss = function(p, v) {
			
			return $(this)
					.css(p, v)
					.css('-moz-' + p, '-moz-' + v)
					.css('-webkit-' + p, '-webkit-' + v)
					.css('-o-' + p, '-o-' + v)
					.css('-ms-' + p, '-ms-' + v);
		
		};

		/**
		 * Does a cross-browser css() call (property).
		 * @param {string} p Property.
		 * @param {string} v Value.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_xcssProperty = function(p, v) {
			
			return $(this)
					.css(p, v)
					.css('-moz-' + p, v)
					.css('-webkit-' + p, v)
					.css('-o-' + p, v)
					.css('-ms-' + p, v);
		
		};

		/**
		 * Does a cross-browser css() call (value).
		 * @param {string} p Property.
		 * @param {string} v Value.
		 * @return {jQuery} Element.
		 */
		$.fn._skel_layers_xcssValue = function(p, v) {
			
			return $(this)
					.css(p, v)
					.css(p, '-moz-' + v)
					.css(p, '-webkit-' + v)
					.css(p, '-o-' + v)
					.css(p, '-ms-' + v);
		
		};

	/**************************************************************************/
	/* Layer Class                                                            */
	/**************************************************************************/

		/**
		 * A layer.
		 * @param {string} id ID.
		 * @param {object} config Config.
		 * @class
		 */
		function Layer(id, config, index) {
		
			var a, x;
		
			this.id = id;
			this.index = index;

			// Config.
				this.config = {
					breakpoints: null,
					states: null,
					position: null,
					side: null,
					animation: 'none',
					orientation: 'none',
					width: 0,
					height: 0,
					zIndex: this.index,
					html: '',
					hidden: false,
					exclusive: true,
					resetScroll: true,
					resetForms: true,
					swipeToHide: true,
					clickToHide: false
				};
				_._.extend(this.config, config);

			// Element.
				this.element = _._.newDiv(this.config.html);
					this.element.id = id;
					this.element._layer = this;
					this.$element = null;

			// Touch stuff.
				this.touchPosX = null;
				this.touchPosY = null;

			// Mark as hidden.
				this.visible = false;

			// Create element.
				x = _._.newElement(
					this.id,
					this.element,
					'skel_layers_hiddenWrapper',
					1
				);

				x.onAttach = function() {
				
					var layer = this.object._layer;
				
					if (!layer.isInitialized())
						layer.init();

					layer.resume();

				};

				x.onDetach = function() {

					var layer = this.object._layer;

					layer.suspend();
					
				};

			// Linked to states?
				if (this.config.states
				&&	this.config.states != _._.sd) {

					// Cache element.
						_._.cacheElement(x);

					// Add to states.
						a = _._.getArray(this.config.states);
						
						_._.iterate(a, function(i) {
							_._.addCachedElementToState(a[i], x);
						});

				}
			
			// Linked to breakpoints?
				else if (this.config.breakpoints) {

					// Cache element.
						_._.cacheElement(x);
	
					// Add to breakpoints.
						a = _._.getArray(this.config.breakpoints);

						_._.iterate(a, function(i) {
							_._.addCachedElementToBreakpoint(a[i], x);
						});
			
				}

			// Not linked to either? Just attach it.
				else
					_._.attachElement(x);
						
		}
		
		/******************************/
		/* Properties                 */
		/******************************/

			/**
			 * Animations.
			 * Each animation requires the following two methods:
			 *    show: Shows the layer, moves it to the visible wrapper.
			 *    hide: Hides the layer, moves it to the hidden wrapper.
			 * @type {object}
			 */
			Layer.prototype.animations = {
			
				/**
				 * None.
				 * No animation. Just shows/hides the layer (overlaps the page).
				 */
				none: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Set up layer element.
							$le
								.scrollTop(0)
								._skel_layers_promote(config.zIndex)
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
					
						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Revert layer element.
							$le
								.hide()
								._skel_layers_demote();
						
						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();

					}
				},

				/**
				 * Overlay (x-axis).
				 * Slides in from the left/right, overlapping the page.
				 */
				overlayX: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Set up layer element.
							$le
								.scrollTop(0)
								._skel_layers_promote(config.zIndex)
								.css(config.side, '-' + _.recalcW(_._.useActive(config.width)) + 'px')
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
						
						// Lock view.
							_.lockView('x');
						
						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();
						
						// Animate.
							window.setTimeout(function() {
								$le._skel_layers_translate((config.side == 'right' ? '-' : '') + _.recalcW(_._.useActive(config.width)), 0);
							}, 50);
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Defocus layer element.
							$le.find('*').trigger('blur', [true]);

						// Animate.
							$le._skel_layers_translateOrigin();
							
						window.setTimeout(function() { 
							
						// Unlock view.
							_.unlockView('x');
							
						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();

						// Revert layer element.
							$le._skel_layers_demote().hide();
					
						}, _.config.speed + 50);

					}
				},

				/**
				 * Overlay (y-axis)
				 * Slides in from the top/bottom, overlapping the page.
				 */
				overlayY: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Set up layer element.
							$le
								.scrollTop(0)
								._skel_layers_promote(config.zIndex)
								.css(config.side, '-' + _.recalcW(_._.useActive(config.height)) + 'px')
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
						
						// Lock view.
							_.lockView('y');
						
						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();
						
						// Animate.
							window.setTimeout(function() {
								$le._skel_layers_translate(0, (config.side == 'bottom' ? '-' : '') + _.recalcW(_._.useActive(config.height)));
							}, 50);
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element;

						// Defocus layer element.
							$le.find('*').trigger('blur', [true]);

						// Animate.
							$le._skel_layers_translateOrigin();
							
						window.setTimeout(function() { 
							
						// Unlock view.
							_.unlockView('y');
							
						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();

						// Revert layer element.
							$le._skel_layers_demote().hide();
					
						}, _.config.speed + 50);

					}
				},

				/**
				 * Push (x-axis)
				 * Slides in from the left/right, pushing the page off the viewport.
				 */
				pushX: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Set up layer element.
							$le
								.scrollTop(0)
								.css(config.side, '-' + _.recalcW(_._.useActive(config.width)) + 'px')
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
							
						// Set up wrappers.
							$w._skel_layers_promote();

						// Lock view.
							_.lockView('x');
						
						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();
						
						// Animate.
							window.setTimeout(function() {
								$le.add($w)._skel_layers_translate((config.side == 'right' ? '-' : '') + _.recalcW(_._.useActive(config.width)), 0);
							}, 50);
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Defocus layer element.
							$le.find('*').trigger('blur', [true]);

						// Animate.
							$le.add($w)._skel_layers_translateOrigin();

						window.setTimeout(function() { 
							
						// Unlock view.
							_.unlockView('x');
							
						// Revert layer element.
							$le.hide();

						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();
					
						// Revert wrappers.
							$w._skel_layers_demote();
									
						}, _.config.speed + 50);

					}
				},
			
				/**
				 * Push (y-axis)
				 * Slides in from the top/bottom, pushing the page off the viewport.
				 */
				pushY: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Set up layer element.
							$le
								.scrollTop(0)
								.css(config.side, '-' + _.recalcH(_._.useActive(config.height)) + 'px')
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
						
						// Lock view.
							_.lockView('y');
						
						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();

						// Animate.
							window.setTimeout(function() {
								$le.add($w)._skel_layers_translate(0, (config.side == 'bottom' ? '-' : '') + _.recalcH(_._.useActive(config.height)));
							}, 50);
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Defocus layer element.
							$le.find('*').trigger('blur', [true]);
					
						// Animate.
							$le.add($w)._skel_layers_translateOrigin();

						window.setTimeout(function() { 
								
						// Unlock view.
							_.unlockView('y');
							
						// Revert layer element.
							$le
								.hide();
								
						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();
							
						}, _.config.speed + 50);

					}
				},

				/**
				 * Reveal (x-axis)
				 * Slides the page left/right, revealing the layer beneath it.
				 */
				revealX: {
					show: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Set up layer element.
							$le
								.scrollTop(0)
								.show();

							if (config.resetForms)
								$le._skel_layers_resetForms();
						
						// Set up wrappers.
							$w._skel_layers_promote();
								
						// Lock view.
							_.lockView('x');

						// Layer => Visible wrapper.
							layer.moveToVisibleWrapper();
						
						// Animate.
							window.setTimeout(function() {
								$w._skel_layers_translate((config.side == 'right' ? '-' : '') + _.recalcW(_._.useActive(config.width)), 0);
							}, 50);
					
					},
					hide: function(layer) {

						var	config = layer.config,
							$le = layer.$element,
							$w = _.cache.wrapper.add(_.cache.visibleWrapper.children());

						// Defocus layer element.
							$le.find('*').trigger('blur', [true]);
							
						// Animate.
							$w._skel_layers_translateOrigin();

						window.setTimeout(function() { 
							
						// Unlock view.
							_.unlockView('x');
						
						// Revert layer element.
							$le.hide();
								
						// Revert wrappers.
							$w._skel_layers_demote();

						// Layer => Hidden wrapper.
							layer.moveToHiddenWrapper();
							
						}, _.config.speed + 50);

					}
				}
				
			}

			/**
			 * Positions.
			 * Where layers can be anchored inside the viewport.
			 * @type {object}
			 */
			Layer.prototype.positions = {
				'top-left':	{
					v: 'top',
					h: 'left',
					side: 'left'
				},
				'top-right': {
					v: 'top',
					h: 'right',
					side: 'right'
				},
				'top': {
					v: 'top',
					h: 'center',
					side: 'top'
				},
				'top-center': {
					v: 'top',
					h: 'center',
					side: 'top'
				},
				'bottom-left': {
					v: 'bottom',
					h: 'left',
					side: 'left'
				},
				'bottom-right': {
					v: 'bottom',
					h: 'right',
					side: 'right'
				},
				'bottom': {
					v: 'bottom',
					h: 'center',
					side: 'bottom'
				},
				'bottom-center': {
					v: 'bottom',
					h: 'center',
					side: 'bottom'
				},
				'left': {
					v: 'center',
					h: 'left',
					side: 'left'
				},
				'center-left': {
					v: 'center',
					h: 'left',
					side: 'left'
				},
				'right': {
					v: 'center',
					h: 'right',
					side: 'right'
				},
				'center-right': {
					v: 'center',
					h: 'right',
					side: 'right'
				}
			};

		/******************************/
		/* Methods                    */
		/******************************/
		
			/**
			 * Shows the layer.
			 */
			Layer.prototype.show = function(instant) {
			
				// If the layer is already visible, make sure it's in the visible wrapper then bail.
				// This bit is needed when the layer's element is reattached by skel, since the attachment location 
				// is always the hidden wrapper (even if the layer is actually visible).
					if (this.visible) {
					
						_.cache.visibleWrapper.append(this.element);
						return;
			
					}
			
				console.log('[skel-layers] ' + this.id + ': showing');
			
				var _this = this,
					config = this.config,
					animation = _._.useActive(config.animation),
					$le = this.$element,
					x;

				// Set size.

					$le
						.css('width', _._.useActive(config.width))
						.css('height', _._.useActive(config.height));
					
					// Hack: iOS fixes.
						if (_._.vars.deviceType == 'ios') {
						
							// If the layer's height is 100%, and it's not a hidden one (ie. it'll be visible when we
							// scroll), pad it a bit to cover up the gap we'd otherwise see (caused by the hiding address bar).
								if (config.height == '100%'
								&&	!config.hidden)
									$le.css('height', '-webkit-calc(' + _._.useActive(config.height) + ' + 70px)');

							// iOS 8 (possibly 7) breaks scrolling on fixed elements on blur. This fugly workaround
							// seems to fix it for the most part.
								$le.on('blur', 'input,select,textarea', function(event, ignore) {
									
									if (ignore)
										return;
									
									window.setTimeout(function() {
										_.cache.hiddenWrapper.append(_this.element);
									
										window.setTimeout(function() {
											_.cache.visibleWrapper.append(_this.element);
										}, 500);
									}, 500);
									
								});
								
						}
					
				// Set position.
					x = this.positions[config.position];

					$le
						.addClass('skel-layer-' + config.position)
						.data('skel-layers-layer-position', config.position);
					
					// Vertical
						switch (x.v) {
						
							case 'top':
								$le.css('top', 0);
								break;
								
							case 'bottom':
								$le.css('bottom', 0);
								break;
								
							case 'center':
								$le
									.css('top', '50%')
									.css('margin-top', '-' + _.getHalf(config.height));
								break;
						
						}
						
					// Horizontal
						switch (x.h) {
						
							case 'left':
								$le.css('left', 0);
								break;
								
							case 'right':
								$le.css('right', 0);
								break;
								
							case 'center':
								$le
									.css('left', '50%')
									.css('margin-left', '-' + _.getHalf(config.width));
								break;
						
						}
						
				// Show it.
					this.animations[animation].show(this);

				// If this isn't a visible layer and it's exclusive, make it the exclusive layer.
					if (config.hidden && config.exclusive) {
						
						_.cache.body.addClass('skel-layers-exclusiveVisible');
						_.cache.exclusiveLayer = this;
					
					}
				
				// Mark as visible.
					this.visible = true;

			};

			/**
			 * Hides the layer.
			 */
			Layer.prototype.hide = function(instant) {

				// If the layer is already hidden, make sure it's in the hidden wrapper then bail.
					if (!this.visible) {

						_.cache.hiddenWrapper.append(this.element);
						return;

					}

				console.log('[skel-layers] ' + this.id + ': hiding');

				var	config = this.config,
					animation = _._.useActive(config.animation);

				// Hide it.
					if (!(animation in this.animations))
						animation = 'none';
				
					this.animations[animation].hide(this);

				// If this is a hidden layer and it's exclusive, make it the exclusive layer.
					if (config.hidden && config.exclusive
					&&	_.cache.exclusiveLayer === this) {
					
						_.cache.body.removeClass('skel-layers-exclusiveVisible');
						_.cache.exclusiveLayer = null;
					
					}
						
				this.visible = false;

			};

			/**
			 * Initializes the layer.
			 * Only called when the layer is resumed for the first time.
			 */
			Layer.prototype.init = function() {

				var	config = this.config,
					$le = $(this.element),
					_this = this,
					x;

				// Initialize.
					$le._skel_layers_init();
						
				// Parse (init).
					$le.find('*').each(function() { _.parseInit($(this)); });

				// Configure.
					$le
						.addClass('skel-layer')
						.data('skel-layers-layer-index', this.index)
						.css('z-index', _.config.baseZIndex)
						.css('position', 'fixed')
						.css('-ms-overflow-style', '-ms-autohiding-scrollbar')
						.css('-webkit-overflow-scrolling', 'touch')
						.hide();

					// Orientation.
						switch (config.orientation) {
						
							case 'vertical':
								$le.css('overflow-y', 'auto');
								break;
								
							case 'horizontal':
								$le.css('overflow-x', 'auto');
								break;
							
							case 'none':
							default:
								break;
						
						}
						
					// Position
						if (!config.position
						||	!(config.position in this.positions))
							config.position = 'top-left';
						
					// Side
						if (!config.side)
							config.side = this.positions[config.position].side;

					// Animation
						if (!config.animation
						||	(typeof config.animation !== 'object' && !(config.animation in this.animations)))
							config.animation = 'none';

					// Click to hide?
						if (config.clickToHide)
							$le.find('a')
								.css('-webkit-tap-highlight-color', 'rgba(0,0,0,0)')
								.on('click.skel-layers', function(event) {
								
									var	t = $(this);
									
									// Ignore? Don't do anything.
										if (t.hasClass('skel-layers-ignore'))
											return;

									// Kill original event.
										event.preventDefault();
										event.stopPropagation();

									// Hide layer.
										_this.hide();

									// Don't actually click? Bail.
										if (t.hasClass('skel-layers-ignoreHref'))
											return;

									// Process href/target.
										var href = t.attr('href'),
											target = t.attr('target');
										
										// Href is set?
											if (typeof href !== 'undefined'
											&&	href != '') {

												window.setTimeout(function() {
													
													if (target == '_blank'
													&&	_._.vars.deviceType != 'wp') // Hack: WP doesn't allow window.open()
														window.open(href);
													else
														window.location.href = href;
												
												}, _.config.speed + 10);
											
											}
									
								});

					// Touch stuff.
						$le
							.on('touchstart', function(e) {
								_this.touchPosX = e.originalEvent.touches[0].pageX;
								_this.touchPosY = e.originalEvent.touches[0].pageY;
							})
							.on('touchmove', function(e) {
							
								if (_this.touchPosX === null
								||	_this.touchPosY === null)
									return;

								var	diffX = _this.touchPosX - e.originalEvent.touches[0].pageX,
									diffY = _this.touchPosY - e.originalEvent.touches[0].pageY,
									th = $le.outerHeight(),
									ts = ($le.get(0).scrollHeight - $le.scrollTop());
								
								// Swipe to hide?
									if (config.hidden && config.swipeToHide) {
										
										var result = false,
											boundary = 20,
											delta = 50;
										
										switch (config.side) {
										
											case 'left':
												result = (diffY < boundary && diffY > (-1 * boundary)) && (diffX > delta);
												break;
										
											case 'right':
												result = (diffY < boundary && diffY > (-1 * boundary)) && (diffX < (-1 * delta));
												break;
										
											case 'top':
												result = (diffX < boundary && diffX > (-1 * boundary)) && (diffY > delta);
												break;
										
											case 'bottom':
												result = (diffX < boundary && diffX > (-1 * boundary)) && (diffY < (-1 * delta));
												break;
										
										}

										if (result) {

											_this.touchPosX = null;
											_this.touchPosY = null;
											_this.hide();
											
											return false;
										
										}
									
									}
									
								// Prevent vertical scrolling past the top or bottom
									if (	($le.scrollTop() == 0 && diffY < 0)
									||		(ts > (th - 2) && ts < (th + 2) && diffY > 0)	)
										return false;

							});

				// Finish init.
					this.$element = $le;
					
				console.log('[skel-layers] ' + this.id + ': layer initialized!');

			};
		
			/**
			 * Determines if the layer is initialized.
			 * @return {bool} If true, the layer has been initialized. If false, the layer hasn't been initialized.
			 */
			Layer.prototype.isInitialized = function() {
			
				return (this.$element !== null);
			
			};

			/**
			 * Determines if the layer is visible.
			 * @return {bool} If true, the layer is visible. If false, the layer isn't visible.
			 */
			Layer.prototype.isVisible = function() {
			
				return this.$element.is(':visible');
			
			};
			
			/**
			 * Moves the layer to the visible wrapper.
			 */
			Layer.prototype.moveToVisibleWrapper = function() {
				_.cache.visibleWrapper.append(this.$element);
			}
			
			/**
			 * Moves the layer to the hidden wrapper.
			 */
			Layer.prototype.moveToHiddenWrapper = function() {
			
				// If layer element doesn't have a parent, it's been suspended (ie. pulled from the DOM tree) so we need to bail out.
					if (!this.$element._skel_layers_hasParent())
						return;

				_.cache.hiddenWrapper.append(this.$element);

			};
		
			/**
			 * Resumes the layer.
			 * Called when skel attaches the layer's element to the DOM.
			 */
			Layer.prototype.resume = function(instant) {

				if (!this.isInitialized())
					return;

				// Parse (resume).
					this.$element.find('*').each(function() { _.parseResume($(this)); });				

				// Not a hidden layer? Show it.
					if (!this.config.hidden)
						this.show(instant);
				
				console.log('[skel-layers] ' + this.id + ': layer resumed');

			};
			
			/**
			 * Suspends the layer.
			 * Called when skel detaches the layer's element to the DOM.
			 */
			Layer.prototype.suspend = function() {
				
				if (!this.isInitialized())
					return;

				// Reset translate.
					this.$element._skel_layers_translateOrigin();

				// Parse (suspend).
					this.$element.find('*').each(function() { _.parseSuspend($(this)); });

				// Visible? Hide.
					if (this.visible)
						this.hide();
				
				console.log('[skel-layers] ' + this.id + ': layer suspended');
				
			};

	/**************************************************************************/
	/* skel-layers Object                                                     */
	/**************************************************************************/
		
		var _ = {

		/******************************/
		/* Properties                 */
		/******************************/

			/**
			 * Object cache.
			 * @type {object}
			 */
			cache: {
			
				// Visible wrapper (where visible layers live).
					visibleWrapper: null,
			
				// body.
					body: null,
			
				// Current exclusive layer.
					exclusiveLayer: null,
			
				// html.
					html: null,
			
				// htmlbody.
					htmlbody: null,
			
				// Hidden Wrapper (where hidden layers live).
					hiddenWrapper: null,
			
				// Layers.
					layers: {},
			
				// window.
					window: null,
			
				// Page wrapper (the original page).
					wrapper: null
			
			},

			/**
			 * Config.
			 * @type {object}
			 */
			config: {
				
				// Base z-index (should be well above anything else on the page).
					baseZIndex: 10000,
				
				// Layers.
					layers: {},
			
				// Animation speed (in ms).
					speed: 250,
				
				// Determines if we should use CSS transforms for animations (= much faster/smoother than CSS).
					transform: true,
				
				// If defined, a list of breakpoints at which CSS transforms are allowed.
					transformBreakpoints: null,
					
				// If defined (as a function), return value is used to determine whether CSS transforms are to be used.
					transformTest: null
				
			},

			/**
			 * Event type.
			 * @type {string}
			 */
			eventType: 'click touchend',
			
		/******************************/
		/* Methods                    */
		/******************************/

			/* API */

				/**
				 * Shows a layer.
				 * @param {string} id Layer ID.
				 */
				show: function(id) {
					_._.DOMReady(function() {
						_.cache.layers[id].show();
					});
				},

				/**
				 * Hides a layer.
				 * @param {string} id Layer ID.
				 */
				hide: function(id) {
					_._.DOMReady(function() {
						_.cache.layers[id].hide();
					});
				},

				/**
				 * Toggles a layer's visibility.
				 * @param {string} id Layer ID.
				 */
				toggle: function(id) {
					_._.DOMReady(function() {

						var layer = _.cache.layers[id];

						if (layer.isVisible())
							layer.hide();
						else
							layer.show();

					});
				},

			/* Main */

				/**
				 * Gets the base font size (in px).
				 * @return {float} Font size.
				 */
				getBaseFontSize: function() {
					
					// Hack: IE<9 doesn't support getComputedStyle so we just return an approximation.
					// Not ideal, but neither is IE8.
						if (_._.vars.IEVersion < 9)
							return 16.5;
						
					return parseFloat(getComputedStyle(_.cache.body.get(0)).fontSize);
					
				},

				/**
				 * Gets half of a CSS measurement (px or %) while preserving its units.
				 * @param {string} n CSS measurement.
				 * @return {string} Half of the original CSS measurement.
				 */
				getHalf: function(n) {

					var i = parseInt(n);

					if (typeof n == 'string'
					&& n.charAt(n.length - 1) == '%')
						return Math.floor(i / 2) + '%';
						
					return Math.floor(i / 2) + 'px';

				},
				
				/**
				 * Locks the viewport. Usually called when a layer is opened.
				 * @param {string} a Orientation.
				 */
				lockView: function(a) {

					_.cache.window._skel_layers_scrollPos = _.cache.window.scrollTop();
				
					// Lock overflow (x-axis only).
						if (a == 'x')
							_.cache.htmlbody.css('overflow-x', 'hidden');
						
					// Lock events.
						_.cache.wrapper.on('touchstart.lock click.lock scroll.lock', function(e) {

							e.preventDefault();
							e.stopPropagation();
							
							if (_.cache.exclusiveLayer)
								_.cache.exclusiveLayer.hide();
						
						});
							
						_.cache.window.on('orientationchange.lock', function(e) {
						
							if (_.cache.exclusiveLayer)
								_.cache.exclusiveLayer.hide();
						
						});

						if (!_._.vars.isMobile)
							window.setTimeout(function() {
								_.cache.window.on('resize.lock scroll.lock', function(e) {
							
									if (_.cache.exclusiveLayer)
										_.cache.exclusiveLayer.hide();
							
								});
							}, _.config.speed + 50);

				},
				
				/**
				 * Parses a child element for actions.
				 * @param {jQuery} x Child element.
				 */
				parseInit: function(x) {

					var a,b;
					
					var	o = x.get(0),
						action = x.attr('data-action'),
						args = x.attr('data-args'),
						arg1, arg2;
					
					if (action && args)
						args = args.split(',');
					
					switch (action) {
						
						/**
						 * Opens/closes a layer.
						 * @arg1 {string} Layer ID.
						 */
						case 'toggleLayer':
						case 'layerToggle':
						
							x
								.css('-webkit-tap-highlight-color', 'rgba(0,0,0,0)')
								.css('cursor', 'pointer');

							a = function(e) {
								e.preventDefault();
								e.stopPropagation();

								if (_.cache.exclusiveLayer) {

									_.cache.exclusiveLayer.hide();
									return false;
								
								}

								var t = $(this), layer = _.cache.layers[args[0]];

								if (layer.isVisible())
									layer.hide();
								else
									layer.show();
							
							};

							x.on(_.eventType, a);
						
							break;
				
						/**
						 * Builds a nav list using links from an existing nav.
						 * @arg1 {string} Existing nav's ID.
						 */
						case 'navList':
							
							arg1 = $('#' + args[0]);
							
							a = arg1.find('a');
							b = [];

							//OpServ Home item hack
							var indent = 0
							var href = "/"
							var text = "Home"
							b.push(
								'<a class="link depth-' + indent + '"' + ( (typeof href !== 'undefined' && href != '') ? ' href="' + href + '"' : '') + '><span class="indent-' + indent + '"></span>' + text + '</a>'
							);

							a.each(function() {
								
								var	t = $(this),
									indent,
									href;
								
								indent = Math.max(0,t.parents('li').length - 1);
								href = t.attr('href');
								console.log(t[0].innerHTML)
								b.push(
                                    '<a class="link depth-' + indent + '"' + ( (typeof href !== 'undefined' && href != '') ? ' href="' + href + '"' : '') + '><span class="indent-' + indent + '"></span>' + t[0].innerHTML + '</a>'
								);
							
							});

                            console.log(b)
							
							if (b.length > 0)
								x.html('<nav>' + b.join('') + '</nav>');
						
							break;

						/* 
						 * Copies text using $.text() from an element.
						 * @arg1 {string} Element ID.
						 */
						case 'copyText':
							
							arg1 = $('#' + args[0]);
							x.html(arg1.text());
							
							break;

						/**
						 * Copies HTML using $.html() from an element.
						 * @arg1 {string} Element ID.
						 */
						case 'copyHTML':

							arg1 = $('#' + args[0]);
							x.html(arg1.html());
							
							break;
						
						/**
						 * Moves an element's (inner) HTML to this one.
						 * @arg1 {string} Element ID.
						 */
						case 'moveElementContents':

							arg1 = $('#' + args[0]);
						
							o._skel_layers_resume = function() {
								arg1.children().each(function() {
									
									var t = $(this);
									
									// Move child element.
										x.append(t);
										
									// Mark as moved.
										t.addClass('skel-layers-moved');

								});
							};
							
							o._skel_layers_suspend = function() {
								x.children().each(function() {
									
									var t = $(this);
									
									// Move child element back.
										arg1.append(t);
								
									// Unmark as moved.
										t.removeClass('skel-layers-moved');
										
									// Refresh.
										_.refresh(t);
								
								});
							};
							
							o._skel_layers_resume();
						
							break;
						
						/**
						 * Moves an element to this one.
						 * @arg1 {string} Element ID.
						 */
						case 'moveElement':

							arg1 = $('#' + args[0]);
						
							o._skel_layers_resume = function() {
								
								// Insert placeholder before arg1.
									$('<div id="skel-layers-placeholder-' + arg1.attr('id') + '" />').insertBefore(arg1);
								
								// Move arg1.
									x.append(arg1);
									
								// Mark arg1 as moved.
									arg1.addClass('skel-layers-moved');

							};
							
							o._skel_layers_suspend = function() {
								
								// Replace placeholder with arg1.
									$('#skel-layers-placeholder-' + arg1.attr('id')).replaceWith(arg1);

								// Unmark arg1 as moved.
									arg1.removeClass('skel-layers-moved');
									
								// Refresh arg1.
									_.refresh(arg1);

							};
							
							o._skel_layers_resume();
						
							break;

						/**
						 * Moves a grid cell to this element.
						 * @arg1 {string} Cell ID.
						 */
						case 'moveCell':

							arg1 = $('#' + args[0]);
							arg2 = $('#' + args[1]);
							
							o._skel_layers_resume = function() {

								// Insert placeholder before arg1.
									$('<div id="skel-layers-placeholder-' + arg1.attr('id') + '" />').insertBefore(arg1);
								
								// Move arg1.
									x.append(arg1);

								// Override arg1 width.
									arg1.css('width', 'auto');

								// Override arg2 width.
									if (arg2)
										arg2._skel_layers_expandCell();

							};
							
							o._skel_layers_suspend = function() {
								
								// Replace placeholder with arg1.
									$('#skel-layers-placeholder-' + arg1.attr('id')).replaceWith(arg1);
									
								// Restore arg1 override.
									arg1.css('width', '');
									
								// Restore arg2 width.
									if (arg2)
										arg2.css('width', '');

							};
							
							o._skel_layers_resume();
						
							break;

						default:
							break;
					}
					
				},

				/**
				 * Tells a child element to resume
				 * @param {jQuery} x Child element.
				 */
				parseResume: function(x) {

					var o = x.get(0);
					
					if (o._skel_layers_resume)
						o._skel_layers_resume();

				},

				/**
				 * Tells a child element to suspend.
				 * @param {jQuery} x Child element.
				 */
				parseSuspend: function(x) {
					
					var o = x.get(0);
					
					if (o._skel_layers_suspend)
						o._skel_layers_suspend();

				},
				
				/**
				 * Converts a CSS measurement to a pixel value relative to a given context.
				 * @param {string} n CSS measurement.
				 * @param {integer} Context.
				 * @return {integer} Pixel value.
				 */
				recalc: function(n, context) {

					var x = _._.parseMeasurement(n),
						y;
					
					switch (x[1]) {
						
						case '%':
							y = Math.floor(context * (x[0] / 100.00));
							break;

						case 'em':
							y = _.getBaseFontSize() * x[0];
							break;
						
						default:
						case 'px':
							y = x[0];
							break;
						
					}
					
					return y;

				},

				/**
				 * Converts a CSS measurement to a pixel value (relative to viewport height).
				 * @param {string} n CSS measurement.
				 * @return {integer} Pixel value.
				 */
				recalcH: function(n) {
					return _.recalc(n, $(window).height());
				},
				
				/**
				 * Converts a CSS measurement to a pixel value (relative to viewport width).
				 * @param {string} n CSS measurement.
				 * @return {integer} Pixel value.
				 */
				recalcW: function(n) {
					return _.recalc(n, $(window).width());
				},
			
				/**
				 * Refreshes Layers.
				 */
				refresh: function(target) {

					var x;

					if (_.config.transform) {
						
						// Move elements with the "skel-layers-fixed" class to visibleWrapper.
							if (target)
								x = target.filter('.skel-layers-fixed:not(.skel-layers-moved)');
							else
								x = $('.skel-layers-fixed:not(.skel-layers-moved)');
							
							x
								._skel_layers_init()
								.appendTo(_.cache.visibleWrapper);
								
					}

				},
				
				/**
				 * Unlocks the viewport. Usually called when a layer is closed.
				 * @param {string} a Orientation.
				 */
				unlockView: function(a) {
					
					// Unlock overflow (x-axis only).
						if (a == 'x')
							_.cache.htmlbody.css('overflow-x', 'visible');
					
					// Unlock events.
						_.cache.wrapper.off('touchstart.lock click.lock scroll.lock');
						_.cache.window.off('orientationchange.lock');
						
						if (!_._.vars.isMobile)
							_.cache.window.off('resize.lock scroll.lock');

				},
			
			/* Init */

				/**
				 * Initializes Layers.
				 */
				init: function() {

					// Apply some config tweaks.

						// Rearrange config.
						// If the incoming config uses the new "convenient" format, rearrange it back into the
						// slightly less convenient format we use internally.

							// Merge config.config (if it exists) with config.
								if ('config' in _.config) {
									
									_._.extend(_.config, _.config.config);
									delete _.config.config;
									
								}
							
							// Move layers to config.layers (if any exist).
								_._.iterate(_.config, function(k) {
									
									if (_.config[k]
									&&	typeof _.config[k] == 'object'
									&&	'position' in _.config[k]) {
										
										_.config.layers[k] = _.config[k];
										delete _.config[k];
										
									}
									
								});

						// Perform transform test (if it's been defined).
							if (_.config.transformTest)
								_.config.transform = (_.config.transformTest)();

						// If transforms are enabled, run additional checks.
							if (_.config.transform) {

								// Hack: Disable transforms on devices that lack proper support for them.
									if ((_._.vars.deviceType == 'android' && _._.vars.deviceVersion < 4)
									||	_._.vars.deviceType == 'wp')
										_.config.transform = false;
										
								// Hack: Disable transforms on IE < 10.
									if (_._.vars.IEVersion < 10)
										_.config.transform = false;

								// Disable transforms if transform breakpoints have been specified but none are active.
									if (_.config.transformBreakpoints
									&& !_._.hasActive(_._.getArray(_.config.transformBreakpoints)))
										_.config.transform = false;
									
							}

					// Initialize objects, transforms.
						_.initObjects();
						_.initTransforms();
					
					// Final initialization stuff.
						_._.DOMReady(function() {
							
							// Initialize layers, includes.
								_.initLayers();
								_.initIncludes();

							// Force a state update.
								_._.updateState();

							// Refresh
								_.refresh();
							
						});
				
				},
				
				/**
				 * Initializes includes.
				 */
				initIncludes: function() {
				
					$('.skel-layers-include').each(function() {
						_.parseInit($(this));
					});
				
				},
			
				/**
				 * Initializes layers.
				 */
				initLayers: function() {

					var config, element, layer, i = 1;

					_._.iterate(_.config.layers, function(id) {

						var e;

						// No position? Bail.
							if (!('position' in _.config.layers[id]))
								return;

						// No element HTML *and* no inline element? Skip layer.
							if (!_.config.layers[id].html
							&&	(e = $('#' + id)).length == 0)
								return;

						// Create layer.
							layer = new Layer(id, _.config.layers[id], i++);
							
						// Add it to cache.
							_.cache.layers[id] = layer;
						
						// Inline element? Use it.
							if (e) {

								e.children().appendTo(layer.element);
								e.remove();
								
							}

					});

				},
				
				/**
				 * Initializes objects.
				 */
				initObjects: function() {
					
					// window.
						_.cache.window = $(window);

					_._.DOMReady(function() {

					// html.
						_.cache.html = $('html');
					
					// body.
						_.cache.body = $('body');

					// htmlbody
						_.cache.htmlbody = $('html,body');
					
					// wrapper.
						_.cache.body.wrapInner('<div id="skel-layers-wrapper" />');
						_.cache.wrapper = $('#skel-layers-wrapper');
						_.cache.wrapper
							.css('position', 'relative')
							.css('left', '0')
							.css('right', '0')
							.css('top', '0')
							._skel_layers_init();

					// hiddenWrapper.
						_.cache.hiddenWrapper = $('<div id="skel-layers-hiddenWrapper" />').appendTo(_.cache.body);
						_.cache.hiddenWrapper
							.css('height', '100%');

						
					// visibleWrapper.
						_.cache.visibleWrapper = $('<div id="skel-layers-visibleWrapper" />').appendTo(_.cache.body);
						_.cache.visibleWrapper
							.css('position', 'relative');

					// Register locations.
						_._.registerLocation('skel_layers_hiddenWrapper', _.cache.hiddenWrapper[0]);
						_._.registerLocation('skel_layers_visibleWrapper', _.cache.visibleWrapper[0]);
						_._.registerLocation('skel_layers_wrapper', _.cache.wrapper[0]);

					// Hack: "autofocus" attribute stops working on webkit when we wrap stuff, so go ahead and force focus here.
						$('[autofocus]').focus();

					});

				},
			
				/**
				 * Initializes transforms.
				 */
				initTransforms: function() {
					
					if (_.config.transform) {
					
						/**
						 * Translates the element back to its point of origin.
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_translateOrigin = function() {
							
							return $(this)._skel_layers_translate(0, 0);

						};				

						/**
						 * Translates the element to specific coordinates.
						 * @param {integer} x Position on x-axis.
						 * @param {integer} y Position on y-axis.
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_translate = function(x, y) {
							return $(this).css('transform', 'translate(' + x + 'px, ' + y + 'px)');
						};

						/**
						 * Initializes the element for animation
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_init = function() {
							
							return $(this)
									.css('backface-visibility', 'hidden')
									.css('perspective', '500')
									._skel_layers_xcss('transition', 'transform ' + (_.config.speed / 1000.00) + 's ease-in-out');
						
						};
					
					}
					else {
						
						var f, origins = [];

						// Forced resets.
							_.cache.window
								.resize(function() {

									if (_.config.speed != 0) {
										
										var t = _.config.speed;
										
										_.config.speed = 0;
										
										window.setTimeout(function() {
											
											// Restore animation speed.
												_.config.speed = t;
											
											// Wipe origins.
												origins = [];
										
										}, t);
									
									}
								
								});

						/**
						 * Translates the element back to its point of origin.
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_translateOrigin = function() {

							for (var i=0; i < this.length; i++) {
								
								var	e = this[i], t = $(e);
								
								if (origins[e.id])
									t.animate(origins[e.id], _.config.speed, 'swing', function() {
									
										// Make sure element is back to its true origin.
											_._.iterate(origins[e.id], function(i) {
												t.css(i, origins[e.id][i]);
											});

										// Reset stuff an animation might've changed.
											_.cache.body
												.css('overflow-x', 'visible');
											_.cache.wrapper
												.css('width', 'auto')
												.css('padding-bottom', 0);
									
									});
							
							}
							
							return $(this);
						};
						
						/**
						 * Translates the element to specific coordinates.
						 * @param {integer} x Position on x-axis.
						 * @param {integer} y Position on y-axis.
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_translate = function(x, y) {

							var i, j, fx, fy;
							
							// Fix x, y.
								x = parseInt(x);
								y = parseInt(y);

							// If we're changing X, change some stuff.
								if (x != 0) {
									
									_.cache.body
										.css('overflow-x', 'hidden');
									_.cache.wrapper
										.css('width', _.cache.window.width());
								
								}
							// Otherwise, set things back to normal (once we're done moving).
								else {
									
									fx = function() {
										
										_.cache.body
											.css('overflow-x', 'visible');
										_.cache.wrapper
											.css('width', 'auto');
									
									};
								
								}
							
							// If we're moving everything *up*, temporarily pad the bottom of the page wrapper.
								if (y < 0)
									_.cache.wrapper
										.css('padding-bottom', Math.abs(y));
							// Otherwise, lose the page wrapper's bottom padding (once we're done moving).
								else
									fy = function() {

										_.cache.wrapper
											.css('padding-bottom', 0);

									};

							// Step through selector's elements.
								for (i=0; i < this.length; i++) {
									
									var	e = this[i],
										t = $(e),
										p;
									
									// Calculate and cache origin (if it hasn't been set yet).
										if (!origins[e.id]) {
											
											if ((p = Layer.prototype.positions[t.data('skel-layers-layer-position')])) {
											
												origins[e.id] = {};
											
												// Vertical
													switch (p.v) {
													
														case 'center':
														case 'top':
															origins[e.id].top = parseInt(t.css('top'));
															break;
															
														case 'bottom':
															origins[e.id].bottom = parseInt(t.css('bottom'));
															break;
														
													}
													
												// Horizontal
													switch (p.h) {
													
														case 'center':
														case 'left':
															origins[e.id].left = parseInt(t.css('left'));
															break;
															
														case 'right':
															origins[e.id].right = parseInt(t.css('right'));
															break;
															
													}
													
											}
											else {
												p = t.position();
												origins[e.id] = { top: p.top, left: p.left };
											}
										
										}

									// Calculate new position.
										a = {};
										
										_._.iterate(origins[e.id], function(i) {
											var v;
											
											switch (i) {
												
												case 'top':
													v = _.recalcH(origins[e.id][i]) + y;
													break;

												case 'bottom':
													v = _.recalcH(origins[e.id][i]) - y;
													break;

												case 'left':
													v = _.recalcW(origins[e.id][i]) + x;
													break;

												case 'right':
													v = _.recalcW(origins[e.id][i]) - x;
													break;
											
											}
											
											a[i] = v;
										
										});
									
									// Move.
										t.animate(a, _.config.speed, 'swing', function() {
											
											// Run functions (if they're set).
												if (fx)
													(fx)();
													
												if (fy)
													(fy)();

										});
								
								}
							
							return $(this);
						
						};

						/**
						 * Initializes the element for animation
						 * @return {jQuery} Element.
						 */
						$.fn._skel_layers_init = function() {
				
							return $(this)
								.css('position', 'absolute');
				
						};
					
					}

				}

		}

		// Expose object.
			return _;

})(jQuery));