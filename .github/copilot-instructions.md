# Mundo da Roça - AI Assistant Guidelines

This is a 2D farming simulation game built with Pygame. Follow these guidelines when working with the codebase:

## Project Structure

- `main.py`: Core game loop and mechanics
- `menu.py`: Menu system and UI
- `save_system.py`: Save/load game state
- `assets/`: Sprite images for crops and characters
  - `{crop_name}/`: Crop growth stage sprites (stages 1-7)

## Key Concepts

### Game State Management
- Game state is persisted in `fazenda_save.json`
- Save format includes:
  - Player money and seed inventory
  - Farm plot states (crops, growth stages, planting times)
  - Fertilized soil locations
  - Last save timestamp

### Crop System
- Three crop types: Milho (corn), Tomate (tomato), Alface (lettuce)
- Each crop has unique:
  - Growth time (3-8 seconds per stage)
  - Purchase price ($8-15)
  - Sale value ($20-40) 
- 7 growth stages:
  - Stages 1-5: Progressive growth
  - Stage 6: Mature (harvestable)
  - Stage 7: Spoiled (must be removed)

### UI Components
- Use `pygame.font.Font(None, size)` for consistent text rendering
- Standard colors defined in `Menu` class
- Game state display in top-left corner
- Shop interface centered when active
- Grid overlay for planting cells

## Development Patterns

### Adding New Crops
1. Create sprite directory in `assets/{crop_name}/`
2. Add growth stage sprites named `{crop_name}_{stage}.png` (stages 1-7)
3. Define crop properties in `TIPOS_SEMENTE` dictionary:
```python
'crop_name': {
    'cor': (R, G, B),
    'preco': purchase_price,
    'valor_colheita': sale_value,
    'tempo_crescimento': growth_time
}
```

### Save System Integration
- Call `SaveSystem.save_game()` when:
  - Player manually saves (S key)
  - Game closes normally
- Load game state with `SaveSystem.load_game()`
- Always handle save/load errors gracefully

### Performance Considerations
- Use sprite scaling at load time, not runtime
- Batch draw calls for repeated elements (grass tiles)
- Update plant states using elapsed time, not frame count

## Key Files Reference
- Core gameplay: `main.py` (700+ lines)
- Menu system: `menu.py` (~250 lines) 
- Save system: `save_system.py` (~150 lines)

## Development Tips
- Test save/load with different game states
- Validate crop timing with all growth stages
- Check grid alignment when adding features
- Consider performance with many active crops