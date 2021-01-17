let add_btn = document.getElementById('add_vote_variant')

let variants_container = document.getElementById('vote_variants')

let variant_blocks = variants_container.getElementsByClassName('list-elem')
let variants_count = document.getElementById('variants_count')

let saved_variant_block = variant_blocks[0].cloneNode(true)
variant_blocks[0].remove()
update_variants_context()

function delete_variant_block(event) {
    event.target.parentNode.remove()
    update_variants_context()
}

function create_variant_block(serial_number) {
    block = saved_variant_block.cloneNode(true)
    let input = block.getElementsByTagName('input')[0]
    input.name = 'variant_' + String(serial_number)
    input.placeholder = 'Вариант ' + String(serial_number + 1)
    block.getElementsByTagName('button')[0].addEventListener('click', delete_variant_block)
    return block
}

function add_new_variant(event) {
    serial_number = variant_blocks.length
    new_variant_block = create_variant_block(serial_number)
    variants_container.appendChild(new_variant_block)
    update_variants_context()
}

function update_variants_context() {
    variants_count.value = variant_blocks.length
    for (let i = 0; i < variant_blocks.length; ++i) {
        block = variant_blocks[i]
        block.getElementsByTagName('button')[0].addEventListener('click', delete_variant_block)
        let input = block.getElementsByTagName('input')[0]
        input.name = 'variant_' + String(i)
        input.placeholder = 'Вариант ' + String(i + 1)
    }
}

add_btn.addEventListener('click', add_new_variant)

for (block of variant_blocks) { block.getElementsByTagName('button')[0].addEventListener('click', delete_variant_block) }